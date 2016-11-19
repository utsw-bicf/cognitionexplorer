from pyramid.response import Response
from pyramid.view import view_config
from snovault import Item
from collections import OrderedDict
from copy import deepcopy
import cgi
import json
import os
from urllib.parse import (
    parse_qs,
    urlencode,
)
from snovault.elasticsearch.interfaces import ELASTIC_SEARCH
import time
from pkg_resources import resource_filename

# TODO: uncomment when ready to try Bek's cache priming solution.
from pyramid.events import subscriber
from .peak_indexer import AfterIndexedExperimentsAndDatasets

import logging
from .search import _ASSEMBLY_MAPPER

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def includeme(config):
    config.add_route('batch_hub', '/batch_hub/{search_params}/{txt}')
    config.add_route('batch_hub:trackdb', '/batch_hub/{search_params}/{assembly}/{txt}')
    config.scan(__name__)

PROFILE_START_TIME = 0  # For profiling within this module

TAB = '\t'
NEWLINE = '\n'
HUB_TXT = 'hub.txt'
GENOMES_TXT = 'genomes.txt'
TRACKDB_TXT = 'trackDb.txt'
BIGWIG_FILE_TYPES = ['bigWig']
BIGBED_FILE_TYPES = ['bigBed']

VISIBLE_DATASET_STATUSES = ["released" ]
VISIBLE_FILE_STATUSES = ["released" ]
VISIBLE_DATASET_TYPES = ["Experiment","Annotation"]

# ASSEMBLY_MAPPINGS is needed to ensure that mm10 and mm10-minimal will get combined into the same trackHub.txt
# This is necessary because mm10 and mm10-minimal are only mm10 at UCSC, so the 2 must be collapsed into one.
ASSEMBLY_MAPPINGS = {
    # any term:       [ set of encoded terms used ]
    "GRCh38":           [ "GRCh38", "GRCh38-minimal" ],
    "GRCh38-minimal":   [ "GRCh38", "GRCh38-minimal" ],
    "hg38":             [ "GRCh38", "GRCh38-minimal" ],
    "GRCh37":           [ "hg19", "GRCh37" ],  # Is GRCh37 ever in encoded?
    "hg19":             [ "hg19", "GRCh37" ],
    "GRCm38":           [ "mm10", "mm10-minimal", "GRCm38" ],  # Is GRCm38 ever in encoded?
    "mm10":             [ "mm10", "mm10-minimal", "GRCm38" ],
    "mm10-minimal":     [ "mm10", "mm10-minimal", "GRCm38" ],
    "GRCm37":           [ "mm9", "GRCm37" ],  # Is GRCm37 ever in encoded?
    "mm9":              [ "mm9", "GRCm37" ],
    "BDGP6":            [ "dm4", "BDGP6" ],
    "dm4":              [ "dm4", "BDGP6" ],
    "BDGP5":            [ "dm3", "BDGP5" ],
    "dm3":              [ "dm3", "BDGP5" ],
    #"WBcel235":         [ "WBcel235" ], # defaults to term: [ term ]
    }


# Supported tokens are the only tokens the code currently know how to look up and swap into text stings.
SUPPORTED_MASK_TOKENS = [
    "{replicate}",         # The replicate that that will be displayed for visualized track: ("rep1", "combined") (AKA rep_tag)
    "{rep_tech}",          # The rep_tech if desired ("rep1_1", "combined")
    "{replicate_number}",  # The replicate number displayed for visualized track: ("1", "0")
    "{biological_replicate_number}",
    "{technical_replicate_number}",
    "{assay_title}",
    "{assay_term_name}",                    # dataset.assay_term_name
    "{annotation_type}",                    # some datasets have annotation type and not assay (higher end trickery)
    "{output_type}",                        # files.output_type
    "{accession}","{experiment.accession}", # "{accession}" is assumed to be experiment.accession
    "{file.accession}",
    "{@id}", "{@type}",                     # dataset only
    "{target}","{target.label}",            # Either is acceptible
    "{target.title}",
    "{target.name}",                        # Used in metadata URLs
    "{biosample_term_name}","{biosample_term_name|multiple}",  # "|multiple": none means multiple
    "{output_type_short_label}",                # hard-coded translation from output_type to very short version Do we want this in schema?
    "{replicates.library.biosample.summary}",   # Idan and Forrest and Cricket are conspiring to move this to dataset.biosample_summary and make it much shorter
    "{replicates.library.biosample.summary|multiple}",   # "|multiple": none means multiple
    "{assembly}",                               # you don't need this in titles, but it is crucial variable and seems to not be being applied correctly in the html generation
    # TODO "{software? or pipeline?}",          # Cricket: "I am stumbling over the fact that we can't distinguish tophat and star produced files"
    # TODO "{phase}",                           # Cricket: "If we get to the point of being fancy in the replication timing, then we need this, otherwise it bundles up in the biosample summary now"
    ]

# Simple tokens are a straight lookup, no questions asked
SIMPLE_DATASET_TOKENS = ["{biosample_term_name}","{accession}","{assay_title}","{assay_term_name}", "{annotation_type}", "{@id}", "{@type}"]

# static group defs are keyed by group title (or special token) and consist of
# tag: (optional) unique terse key for referencing group
# groups: (optional) { subgroups keyed by subgroup title }
# group_order: (optional) [ ordered list of subgroup titles ]
# other definitions

# live group defs are keyed by tag and are the transformed in memory version of static defs
# title: (required) same as the static group's key
# groups: (if appropriate) { subgroups keyed by subgroup tag }
# group_order: (if appropriate) [ ordered list of subgroup tags ]

VIS_DEFS_FOLDER = "static/vis_defs/"
VIS_DEFS_BY_TYPE = {}
COMPOSITE_VIS_DEFS_DEFAULT = {}


def lookup_token(token,dataset,a_file=None):
    '''Encodes the string to swap special characters and remove spaces.'''

    if token not in SUPPORTED_MASK_TOKENS:
        log.warn("Attempting to look up unexpected token: '%s'" % token)
        return "unknown token"

    if token in SIMPLE_DATASET_TOKENS:
        term = dataset.get(token[1:-1])
        if term is None:
            term = "Unknown " + token[1:-1].split('_')[0].capitalize()
        return term
    elif token == "{experiment.accession}":
        return dataset['accession']
    elif token in ["{target}","{target.label}","{target.name}","{target.title}"]:
        target = dataset.get('target',{})
        if isinstance(target,list):
            if len(target) > 0:
                target = target[0]
            else:
                target = {}
        if token.find('.') > -1:
            sub_token = token.strip('{}').split('.')[1]
        else:
            sub_token = "label"
        return target.get(sub_token,"Unknown Target")
        #if token == "{target.name}":
        #    return target.get('name',"Unknown Target")
        #return target.get('label',"Unknown Target")
    elif token in ["{target.name}"]:
        target = dataset.get('target',{})
        if isinstance(target,list):
            if len(target) > 0:
                target = target[0]
            else:
                target = {}
        return target.get('label',"Unknown Target")
    elif token in ["{replicates.library.biosample.summary}","{replicates.library.biosample.summary|multiple}"]:
        term = None
        replicates = dataset.get("replicates",[])
        if replicates:
            term = replicates[0].get("library",{}).get("biosample",{}).get("summary")
        if term is None:
            term = dataset.get("{biosample_term_name}")
        if term is None:
            if token.endswith("|multiple}"):
                term = "multiple biosamples"
            else:
                term = "Unknown Biosample"
        return term
    elif token == "{biosample_term_name|multiple}":
        return dataset.get("biosample_term_name","multiple biosamples")
    # TODO: rna_species
    #elif token == "{rna_species}":
    #    if replicates.library.nucleic_acid = polyadenylated mRNA
    #       rna_species = polyA RNA
    #    elseif replicates.library.nucleic_acid = RNA
    #       if polyadenylated mRNA in replicates.library.depleted_in_term_name
    #               rna_species = polyA depleted RNA
    #       else
    #               rna_species = total RNA
    elif a_file is not None:
        if token == "{file.accession}":
            return a_file['accession']
        elif token == "{output_type}":
            return a_file['output_type']
        elif token == "{output_type_short_label}":
            output_type = a_file['output_type']
            return OUTPUT_TYPE_8CHARS.get(output_type,output_type)
        elif token == "{replicate}":
            rep_tag = a_file.get("rep_tag")
            if rep_tag is not None:
                while len(rep_tag) > 4:
                    if rep_tag[3] != '0':
                        break
                    rep_tag = rep_tag[0:3] + rep_tag[4:]
                return rep_tag
            rep_tech = a_file.get("rep_tech")
            if rep_tech is not None:
                return rep_tech.split('_')[0]  # Should truncate tech_rep
            rep_tech = rep_for_file(a_file)
            return rep_tech.split('_')[0]  # Should truncate tech_rep
        elif token == "{replicate_number}":
            rep_tag = a_file.get("rep_tag",a_file.get("rep_tech",rep_for_file(a_file)))
            if not rep_tag.startswith("rep"):
                return "0"
            return rep_tag[3:].split('_')[0]
        elif token == "{biological_replicate_number}":
            rep_tech = a_file.get("rep_tech",rep_for_file(a_file))
            if not rep_tech.startswith("rep"):
                return "0"
            return rep_tech[3:].split('_')[0]
        elif token == "{technical_replicate_number}":
            rep_tech = a_file.get("rep_tech",rep_for_file(a_file))
            if not rep_tech.startswith("rep"):
                return "0"
            return rep_tech.split('_')[1]
        elif token == "{rep_tech}":
            return a_file.get("rep_tech",rep_for_file(a_file))
        else:
            return ""
    else:
        log.warn('Untranslated token: "%s"' % token)
        return "unknown"

def convert_mask(mask,dataset,a_file=None):
    '''Given a mask with one or more known {term_name}s, replaces with values.'''
    working_on = mask
    chars = len(working_on)
    while chars > 0:
        beg_ix = working_on.find('{')
        if beg_ix == -1:
            break
        end_ix = working_on.find('}')
        if end_ix == -1:
            break
        term = lookup_token(working_on[beg_ix:end_ix+1],dataset,a_file=a_file)
        new_mask = []
        if beg_ix > 0:
            new_mask = working_on[0:beg_ix]
        new_mask += "%s%s" % (term,working_on[end_ix+1:])
        chars = len(working_on[end_ix+1:])
        working_on = ''.join(new_mask)

    return working_on


def strip_comments(line,ws_too=False):
    """
    Strips comments from a line (and opptionally leading/trailing whitespace).
    """
    pound = -1
    ix = 0
    while True:
        pound = line[ix:].find('#',pound + 1)
        if pound == -1:
            break
        pound = ix + pound
        if pound == 0:
            return ''
        if line[ pound - 1 ] != '\\':
            line = line[ 0:pound ]
            break  
        else: #if line[ pound - 1 ] == '\\': # ignore '#' and keep looking
            ix = pound + 1
            #line = line[ 0:pound - 1 ] + line[ pound: ]           
    if ws_too:
        line = line.strip()
    return line 

def gulp_file_strip_comments(path):
    '''Reads in entire file stripping any # comments and returns string.'''
    blob = ''
    with open(path) as fh:
        for line in fh:
            line = line.rstrip('\n')
            while line.endswith('\\'): # Support for continuation lines
                line = line[:-1] + next(fn).strip()
            line = strip_comments(line,False)
            if line == '':
                continue
            blob += line + '\n'
    return blob

    
def load_vis_defs():
    '''Loads 'vis_defs' (visualization definitions by assay type) from a static file.'''
    global VIS_DEFS_FOLDER
    global VIS_DEFS_BY_TYPE
    global COMPOSITE_VIS_DEFS_DEFAULT
    folder = resource_filename(__name__, VIS_DEFS_FOLDER)
    files = os.listdir(folder)
    for filename in files:
        if filename.endswith('.json'):
            log.debug('Preparing to load %s' % (filename))
            vis_def = json.loads(gulp_file_strip_comments(folder + filename))
            if vis_def:
                VIS_DEFS_BY_TYPE.update(vis_def)

def get_vis_type(dataset):
    '''returns the best static composite definition set, based upon dataset.'''
    global VIS_DEFS_BY_TYPE
    if not VIS_DEFS_BY_TYPE:
        load_vis_defs()
        
    assay = dataset.get("assay_term_name",'none')

    if isinstance(assay,list):
        if len(assay) == 1:
            assay = assay[0]
        else:
            log.warn("assay_term_name for %s is unexpectedly a list %s" % (dataset['accession'],str(assay)))
            return "opaque"
            
    # simple rule defined in most vis_defs
    for vis_type in sorted(VIS_DEFS_BY_TYPE.keys(), reverse=True): # Reverse pushes anno to bottom
        if "rule" in VIS_DEFS_BY_TYPE[vis_type]:
            rule = VIS_DEFS_BY_TYPE[vis_type]["rule"].replace('{assay_term_name}',assay)
            if rule.find('{') != -1:
                rule = convert_mask(rule,dataset)
            if eval(rule):
                return vis_type

    # Ugly rules:
    if assay in ["RNA-seq","single cell isolation followed by RNA-seq"]:
        reps = dataset.get("replicates",[]) # NOTE: overly cautious due to test failures with incomplete test data
        if len(reps) < 1:
            log.warn("Could not distinguish between long and short RNA for %s because there are no replicates.  Defaulting to short." % (dataset.get("accession")))
            return "SRNA"  # this will be more noticed if there is a mistake
        size_range = reps[0].get("library",{}).get("size_range","")
        if size_range.startswith('>'):
            try:
                min_size = int(size_range[1:])
                max_size = min_size
            except:
                log.warn("Could not distinguish between long and short RNA for %s.  Defaulting to short." % (dataset.get("accession")))
                return "SRNA"  # this will be more noticed if there is a mistake
        elif size_range.startswith('<'):
            try:
                max_size = int(size_range[1:]) - 1
                min_size = 0
            except:
                log.warn("Could not distinguish between long and short RNA for %s.  Defaulting to short." % (dataset.get("accession")))
                return "SRNA"  # this will be more noticed if there is a mistake
        else:
            try:
                sizes = size_range.split('-')
                min_size = int(sizes[0])
                max_size = int(sizes[1])
            except:
                log.warn("Could not distinguish between long and short RNA for %s.  Defaulting to short." % (dataset.get("accession")))
                return "SRNA"  # this will be more noticed if there is a mistake
        if max_size <= 200 and max_size != min_size:
            return "SRNA"
        elif min_size >= 150:
            return "LRNA"
        elif (min_size + max_size)/2 >= 235: # This is some wicked voodoo (SRNA:108-347=227; LRNA:155-315=235)
            return "LRNA"
        else:
            return "SRNA"

    log.warn("%s (assay:'%s') has undefined vis_type" % (dataset['accession'],assay))
    return "opaque" # This becomes a dict key later so None is not okay

# TODO:
# ENCSR000BBI (assay:'comparative genomic hybridization by array') has undefined vis_type
# ENCSR000DBZ (assay:'FAIRE-seq') has undefined vis_type
# ENCSR901QEL (assay:'protein sequencing by tandem mass spectrometry assay') has undefined vis_type
# ENCSR000AWN (assay:'transcription profiling by array assay') has undefined vis_type
# ENCSR066KKK (assay:'Repli-chip') has undefined vis_type
# ENCSR935ULX (assay:'Repli-seq') has undefined vis_type
# ENCSR000AYD (assay:'RIP-chip') has undefined vis_type
# ENCSR000CWU (assay:'RIP-seq') has undefined vis_type
# ENCSR000BCM (assay:'RNA-PET') has undefined vis_type

EXP_GROUP = "Experiment"
DEFAULT_EXPERIMENT_GROUP = { "tag": "EXP", "groups": { "one": { "title_mask": "{accession}", "url_mask": "experiments/{accession}"} } }

def lookup_vis_defs(vis_type):
    '''returns the best static composite definition set, based upon dataset.'''
    global VIS_DEFS_BY_TYPE
    global COMPOSITE_VIS_DEFS_DEFAULT
    vis_def = VIS_DEFS_BY_TYPE.get(vis_type, COMPOSITE_VIS_DEFS_DEFAULT )
    if EXP_GROUP not in vis_def["other_groups"]["groups"]:
        vis_def["other_groups"]["groups"][EXP_GROUP] = DEFAULT_EXPERIMENT_GROUP
    if "sortOrder" in vis_def and EXP_GROUP not in vis_def["sortOrder"]:
        vis_def["sortOrder"].append(EXP_GROUP)
    return vis_def

PENNANTS = {
    "NHGRI":  "https://www.encodeproject.org/static/img/pennant-nhgri.png https://www.encodeproject.org/ \"This trackhub was automatically generated from the files and metadata found at the ENCODE portal\"",
    "ENCODE": "https://www.encodeproject.org/static/img/pennant-encode.png https://www.encodeproject.org/ \"This trackhub was automatically generated from the ENCODE files and metadata found at the ENCODE portal\"",
    "modENCODE":"https://www.encodeproject.org/static/img/pennant-encode.png https://www.encodeproject.org/ \"This trackhub was automatically generated from the modENCODE files and metadata found at the ENCODE portal\"",
    "GGR":    "https://www.encodeproject.org/static/img/pennant-ggr.png https://www.encodeproject.org/ \"This trackhub was automatically generated from the Genomics of Gene Regulation files files and metadata found at the ENCODE portal\"",
    "REMC":   "https://www.encodeproject.org/static/img/pennant-remc.png https://www.encodeproject.org/ \"This trackhub was automatically generated from the Roadmap Epigentics files and metadata found at the ENCODE portal\"",
    #"Roadmap":   "encodeThumbnail.jpg https://www.encodeproject.org/ \"This trackhub was automatically generated from the Roadmap files and metadata found at https://www.encodeproject.org/\"",
    #"modERN":   "encodeThumbnail.jpg https://www.encodeproject.org/ \"This trackhub was automatically generated from the modERN files and metadata found at https://www.encodeproject.org/\"",
    }
def find_pennent(dataset):
    '''Returns an appropriate pennantIcon given dataset's award'''
    project = dataset.get("award",{}).get("project","NHGRI")
    return PENNANTS.get(project,PENNANTS.get("NHGRI"))


SUPPORTED_SUBGROUPS = [ "Biosample", "Targets", "Assay", "Replicates", "Views", EXP_GROUP ]

SUPPORTED_TRACK_SETTINGS = [
    "type","visibility","longLabel","shortLabel","color","altColor","allButtonPair","html"
    "scoreFilter","spectrum",
    "viewLimits","autoScale","negateValues","maxHeightPixels","windowingFunction","transformFunc",
    ]
COMPOSITE_SETTINGS = ["longLabel","shortLabel","visibility","pennantIcon","allButtonPair","html"]
VIEW_SETTINGS = SUPPORTED_TRACK_SETTINGS
TRACK_SETTINGS = ["bigDataUrl","longLabel","shortLabel","type","color","altColor"]


OUTPUT_TYPE_8CHARS = {
    #"idat green channel": "idat gr",     # raw data
    #"idat red channel": "idat rd",       # raw data
    #"reads":"reads",                     # raw data
    #"intensity values": "intnsty",       # raw data
    #"reporter code counts": "rcc",       # raw data
    #"alignments":"aln",                  # our plan is not to visualize alignments for now
    #"unfiltered alignments":"unflt aln", # our plan is not to visualize alignments for now
    #"transcriptome alignments":"tr aln", # our plan is not to visualize alignments for now
    "minus strand signal of all reads":     "all -",
    "plus strand signal of all reads":      "all +",
    "signal of all reads":                  "all sig",
    "normalized signal of all reads":       "normsig",
    #"raw minus strand signal":"raw -",   # these are all now minus signal of all reads
    #"raw plus strand signal":"raw +",    # these are all now plus signal of all reads
    "raw signal":                           "raw sig",
    "raw normalized signal":                "nraw",
    "read-depth normalized signal":         "rdnorm",
    "control normalized signal":            "ctlnorm",
    "minus strand signal of unique reads":  "unq -",
    "plus strand signal of unique reads":   "unq +",
    "signal of unique reads":               "unq sig",
    "signal p-value":                       "pval sig",
    "fold change over control":             "foldchg",
    "exon quantifications":                 "exon qt",
    "gene quantifications":                 "gene qt",
    "microRNA quantifications":             "miRNA qt",
    "transcript quantifications":           "trsct qt",
    "library fraction":                     "lib frac",
    "methylation state at CpG":             "mth CpG",
    "methylation state at CHG":             "mth CHG",
    "methylation state at CHH":             "mth CHH",
    "enrichment":                           "enrich",
    "replication timing profile":           "repli tm",
    "variant calls":                        "vars",
    "filtered SNPs":                        "f SNPs",
    "filtered indels":                      "f indel",
    "hotspots":                             "hotspt",
    "long range chromatin interactions":    "lrci",
    "chromatin interactions":               "ch int",
    "topologically associated domains":     "tads",
    "genome compartments":                  "compart",
    "open chromatin regions":               "open ch",
    "filtered peaks":                       "filt pk",
    "filtered regions":                     "filt reg",
    "DHS peaks":                            "DHS pk",
    "peaks":                                "peaks",
    "replicated peaks":                     "rep pk",
    "RNA-binding protein associated mRNAs": "RBP RNA",
    "splice junctions":                     "splice",
    "transcription start sites":            "tss",
    "predicted enhancers":                  "pr enh",
    "candidate enhancers":                  "can enh",
    "candidate promoters":                  "can pro",
    "predicted forebrain enhancers":        "fb enh",    # plan to fix these
    "predicted heart enhancers":            "hrt enh",       # plan to fix these
    "predicted whole brain enhancers":      "wb enh",  # plan to fix these
    "candidate regulatory elements":        "can re",
    #"genome reference":"ref",           # references not to be viewed
    #"transcriptome reference":"tr ref", # references not to be viewed
    #"transcriptome index":"tr rix",     # references not to be viewed
    #"tRNA reference":"tRNA",            # references not to be viewed
    #"miRNA reference":"miRNA",          # references not to be viewed
    #"snRNA reference":"snRNA",          # references not to be viewed
    #"rRNA reference":"rRNA",            # references not to be viewed
    #"TSS reference":"TSS",              # references not to be viewed
    #"reference variants":"var",         # references not to be viewed
    #"genome index":"ref ix",            # references not to be viewed
    #"female genome reference":"XX ref", # references not to be viewed
    #"female genome index":"XX rix",     # references not to be viewed
    #"male genome reference":"XY ref",   # references not to be viewed
    #"male genome index":"XY rix",       # references not to be viewed
    #"spike-in sequence":"spike",        # references not to be viewed
    "optimal idr thresholded peaks":        "oIDR pk",
    "conservative idr thresholded peaks":   "cIDR pk",
    "enhancer validation":                  "enh val",
    "semi-automated genome annotation":     "saga"
    }

BIOSAMPLE_COLOR = {
    "induced pluripotent stem cell line":   {"color":"80,49,120",   "altColor": "107,95,102" }, # Purple
    "stem cell":                            { "color":"0,107,27",   "altColor": "0.0,77,20"  }, # Dark Green
    "GM12878":                              { "color":"153,38,0",   "altColor": "115,31,0"   }, # Dark Orange-Red
    "H1-hESC":                              { "color":"0,107,27",   "altColor": "0,77,20"    },  # Dark Green
    "K562":                                 { "color":"46,0,184",   "altColor": "38,0,141"   }, # Dark Blue
    "keratinocyte":                         { "color":"179,0,134",  "altColor": "154,0,113"  }, # Darker Pink-Purple
    "HepG2":                                { "color":"189,0,157",  "altColor": "189,76,172" }, # Pink-Purple
    "HeLa-S3":                              { "color":"0,119,158",  "altColor": "0,94,128"   }, # Greenish-Blue
    "HeLa":                                 { "color":"0,119,158",  "altColor": "0,94,128"   }, # Greenish-Blue
    "A549":                                 { "color":"204,163,0",  "altColor": "218,205,22" }, # Dark Yellow replacing: "255,241,26", "altColor": "218,205,22" }, # Yellow
    "endothelial cell of umbilical vein":   { "color":"224,75,0",   "altColor": "179,60,0"   },  # Pink
    "MCF-7":                                { "color":"22,219,206", "altColor": "18,179,168" }, # Cyan
    "SK-N-SH":                              { "color":"255,115,7",  "altColor": "218,98,7"   },  # Orange
    "IMR-90":                               { "color":"6,62,218",   "altColor": "5,52,179"   },  # Blue
    "CH12.LX":                              { "color":"86,180,233", "altColor": "76,157,205" }, # Dark Orange-Red
    "MEL cell line":                        { "color":"46,0,184",   "altColor": "38,0,141"   }, # Dark Blue
    "brain":                                { "color":"105,105,105","altColor": "77,77,77"   }, # Grey
    "eye":                                  { "color":"105,105,105","altColor": "77,77,77"   }, # Grey
    "spinal cord":                          { "color":"105,105,105","altColor": "77,77,77"   }, # Grey
    "olfactory organ":                      { "color":"105,105,105","altColor": "77,77,77"   }, # Grey
    "esophagus":                            { "color":"230,159,0",  "altColor": "179,125,0"  }, # Mustard
    "stomach":                              { "color":"230,159,0",  "altColor": "179,125,0"  }, # Mustard
    "liver":                                { "color":"230,159,0",  "altColor": "179,125,0"  }, # Mustard
    "pancreas":                             { "color":"230,159,0",  "altColor": "179,125,0"  }, # Mustard
    "large intestine":                      { "color":"230,159,0",  "altColor": "179,125,0"  }, # Mustard
    "small intestine":                      { "color":"230,159,0",  "altColor": "179,125,0"  }, # Mustard
    "gonad":                                { "color":"0.0,158,115","altColor": "0.0,125,92" }, # Darker Aquamarine
    "mammary gland":                        { "color":"0.0,158,115","altColor": "0.0,125,92" }, # Darker Aquamarine
    "prostate gland":                       { "color":"0.0,158,115","altColor": "0.0,125,92" }, # Darker Aquamarine
    "ureter":                               { "color":"204,121,167","altColor": "166,98,132" }, # Grey-Pink
    "urinary bladder":                      { "color":"204,121,167","altColor": "166,98,132" }, # Grey-Pink
    "kidney":                               { "color":"204,121,167","altColor": "166,98,132" }, # Grey-Pink
    "muscle organ":                         { "color":"102,50,200 ","altColor": "81,38,154"  }, # Violet
    "tongue":                               { "color":"102,50,200", "altColor": "81,38,154"  }, # Violet
    "adrenal gland":                        { "color":"189,0,157",  "altColor": "154,0,128"  }, # Pink-Purple
    "thyroid gland":                        { "color":"189,0,157",  "altColor": "154,0,128"  }, # Pink-Purple
    "lung":                                 { "color":"145,235,43", "altColor": "119,192,35" }, # Mossy green
    "bronchus":                             { "color":"145,235,43", "altColor": "119,192,35" }, # Mossy green
    "trachea":                              { "color":"145,235,43", "altColor": "119,192,35" }, # Mossy green
    "nose":                                 { "color":"145,235,43", "altColor": "119,192,35" }, # Mossy green
    "placenta":                             { "color":"153,38,0",   "altColor": "102,27,0"   }, # Orange-Brown
    "extraembryonic structure":             { "color":"153,38,0",   "altColor": "102,27,0"   }, # Orange-Brown
    "thymus":                               { "color":"86,180,233", "altColor": "71,148,192" }, # Baby Blue
    "spleen":                               { "color":"86,180,233", "altColor": "71,148,192" }, # Baby Blue
    "bone element":                         { "color":"86,180,233", "altColor": "71,148,192" }, # Baby Blue
    "blood":                                { "color":"86,180,233", "altColor": "71,148,192" },  # Baby Blue This follows UCSC but I want it to be red
    "blood vessel":                         { "color":"214,0,0",    "altColor": "214,79,79"  }, # Red
    "heart":                                { "color":"214,0,0",    "altColor": "214,79,79"  }, # Red
    "lymphatic vessel":                     { "color":"214,0,0",    "altColor": "214,79,79"  }, # Red
    "skin of body":                         { "color":"74,74,21",   "altColor": "102,102,44" } # Brown
    }

def lookup_colors(dataset):
    '''Using the mask, determine which color table to use.'''
    color = None
    altColor = None
    coloring = {}
    biosample_term = dataset.get('biosample_type')
    if biosample_term is not None:
        if isinstance(biosample_term,list):
            if len(biosample_term) == 1:
                biosample_term = biosample_term[0]
            else:
                log.warn("%s has biosample_type %s that is unexpectedly a list" % (dataset['accession'],str(biosample_term)))
                biosample_term = "unknown"  # really only seen in test data!
        coloring = BIOSAMPLE_COLOR.get(biosample_term,{})
    if not coloring:
        biosample_term = dataset.get('biosample_term_name')
        if biosample_term is not None:
            if isinstance(biosample_term,list):
                if len(biosample_term) == 1:
                    biosample_term = biosample_term[0]
                else:
                    log.warn("%s has biosample_term_name %s that is unexpectedly a list" % (dataset['accession'],str(biosample_term)))
                    biosample_term = "unknown"  # really only seen in test data!
            coloring = BIOSAMPLE_COLOR.get(biosample_term,{})
    if not coloring:
        organ_slims = dataset.get('organ_slims',[])
        if len(organ_slims) > 1:
            coloring = BIOSAMPLE_COLOR.get(organ_slims[1])
    if coloring:
        assert("color" in coloring)
        if "altColor" not in coloring:
            color = coloring["color"]
            shades = color.split(',')
            red = int(shades[0]) / 2
            green = int(shades[1]) / 2
            blue = int(shades[2]) / 2
            altColor = "%d,%d,%d" % (red,green,blue)
            coloring["altColor"] = altColor

    return coloring

def add_living_color(live_settings, dataset):
    '''Adds color and altColor.  Note that altColor is only added if color is found.'''
    colors = lookup_colors(dataset)
    if colors and "color" in colors:
        live_settings["color"] = colors["color"]
        if "altColor" in colors:
            live_settings["altColor"] = colors["altColor"]

def sanitize_char(c,exceptions=[ '_' ],htmlize=False,numeralize=False):
    '''Pass through for 0-9,A-Z.a-z,_, but then either html encodes, numeralizes or removes special characters.'''
    n = ord(c)
    if n >= 47 and n <= 57: # 0-9
        return c
    if n >= 65 and n <= 90: # A-Z
        return c
    if n >= 97 and n <= 122: # a-z
        return c
    if c in exceptions:
        return c
    if n == 32:              # space
        return '_'
    if htmlize:
        return "&#%d;" % n
    if numeralize:
        return "%d" % n

    return ""

def sanitize_label(s):
    '''Encodes the string to swap special characters and leaves spaces alone.'''
    new_s = ""      # longLabel and shorLabel can have spaces and some special characters
    for c in s:
        new_s += sanitize_char(c,[ ' ', '_','.','-','(',')','+' ],htmlize=True)
    return new_s

def sanitize_title(s):
    '''Encodes the string to swap special characters and replace spaces with '_'.'''
    new_s = ""      # Titles appear in tag=title pairs and cannot have spaces
    for c in s:
        new_s += sanitize_char(c,[ '_','.','-','(',')','+' ],htmlize=True)
    return new_s

def sanitize_tag(s):
    '''Encodes the string to swap special characters and remove spaces.'''
    new_s = ""
    first = True
    for c in s:
        new_s += sanitize_char(c,numeralize=True)
        if first:
            if new_s.isdigit(): # tags cannot start with digit.
                new_s = 'z' + new_s
            first = False
    return new_s

def sanitize_name(s):
    '''Encodes the string to remove special characters swap spaces for underscores.'''
    new_s = ""
    first = True
    for c in s:
        new_s += sanitize_char(c)
    return new_s

def add_to_es(request,comp_id,composite):
    '''Adds a composite json blob to elastic-search'''
    key="vis_composite"
    es = request.registry.get(ELASTIC_SEARCH, None)
    if not es:
        return
    if not es.indices.exists(key):
        es.indices.create(index=key, body={ 'index': { 'number_of_shards': 1 } })
        mapping = { 'default': {    "_all" :    { "enabled": False },
                                    "_source":  { "enabled": True },
        #                            "_id":      { "index":  "not_analyzed", "store" : True },
        #                            "_ttl":     { "enabled": True, "default" : "1d" },
                               } }
        es.indices.put_mapping(index=key, doc_type='default', body=mapping )
        log.debug("created %s index" % key)
    es.index(index=key, doc_type='default', body=composite, id=comp_id)

def get_from_es(request,comp_id):
    '''Returns composite json blob from elastic-search, or None if not found.'''
    key="vis_composite"
    es = request.registry.get(ELASTIC_SEARCH, None)
    if es and es.indices.exists(key):
        try:
            result = es.get(index=key, doc_type='default', id=comp_id)
            return result['_source']
        except:
            pass
    return None

def search_es(request,ids):
    '''Returns a list of composites from elastic-search, or None if not found.'''
    key="vis_composite"
    es = request.registry.get(ELASTIC_SEARCH, None)
    if es and es.indices.exists(key):
        try:
            query = { "query": { "ids" : { "values" : ids } } }
            res = es.search(body=query, index=key, doc_type='default',size=99999) # Consider size=200
            hits = res.get("hits",{}).get("hits",[])
            results = {}
            for hit in hits:
                results[hit["_id"]] = hit["_source"] # make this a generator? No... len(results)
            log.debug("ids found: %d   %.3f secs" % (len(results),(time.time() - PROFILE_START_TIME)))
            return results
        except:
            pass
    return {}

def rep_for_file(a_file):
    '''Determines best rep_tech or rep for a file.'''

    # Starting with a little cheat for rare cases where techreps are compared instead of bioreps
    if a_file.get("file_format_type","none") in ["idr_peak"]:
        return "combined"
    if a_file['output_type'].endswith("idr thresholded peaks"):
        return "combined"

    bio_rep = 0
    tech_rep = 0
    if "replicate" in a_file:
        bio_rep = a_file["replicate"]["biological_replicate_number"]
        tech_rep = a_file["replicate"]["technical_replicate_number"]

    elif "tech_replicates" in a_file:
        # Do we want to make rep1_1.2.3 ?  Not doing it now
        tech_reps = a_file["tech_replicates"]
        if len(tech_reps) == 1:
            bio_rep = int(tech_reps[0].split('_')[0])
            tech_reps = tech_reps[0][2:]
            if len(tech_reps) == 1:
                tech_rep = int(tech_reps)
        elif len(tech_reps) > 1:
            bio = 0
            for tech in tech_reps:
                if bio == 0:
                    bio = int(tech.split('_')[0])
                elif bio != int(tech.split('_')[0]):
                    bio = 0
                    break
            if bio > 0:
                bio_rep = bio

    elif "biological_replicates" in a_file:
        bio_reps = a_file["biological_replicates"]
        if len(bio_reps) == 1:
            bio_rep = bio_reps[0]

    if bio_rep == 0:
        return "combined"

    rep = "rep%d" % bio_rep
    if tech_rep > 0:
        rep += "_%d" % tech_rep
    return rep

def handle_negateValues(live_settings, defs, dataset, composite):
    '''If negateValues is set then adjust some settings like color'''
    if live_settings.get("negateValues","off") == "off":
        return

    # need to swap color and altColor
    color = live_settings.get("color",composite.get("color"))
    if color is not None:
        altColor = live_settings.get("altColor",composite.get("altColor",color))
        live_settings["color"] = altColor
        live_settings["altColor"] = color

    # view limits need to change because numbers are all negative
    viewLimits = live_settings.get("viewLimits")
    if viewLimits is not None:
        low_high = viewLimits.split(':')
        if len(low_high) == 2:
            live_settings["viewLimits"] = "%d:%d" % (int(low_high[1]) * -1,int(low_high[0]) * -1)
    viewLimitsMax = live_settings.get("viewLimitsMax")
    if viewLimitsMax is not None:
        low_high = viewLimitsMax.split(':')
        if len(low_high) == 2:
            live_settings["viewLimitsMax"] = "%d:%d" % (int(low_high[1]) * -1,int(low_high[0]) * -1)

def generate_live_groups(composite,title,group_defs,dataset,rep_tags=[]):
    '''Recursively populates live (in memory) groups from static group definitions'''
    live_group = {}
    tag = group_defs.get("tag",title)
    live_group["title"] = title
    live_group["tag"] = tag
    for key in group_defs.keys():
        if key not in ["groups","group_order"]: # leave no trace of subgroups keyed by title
            live_group[key] = deepcopy(group_defs[key])

    if title == "replicate": # transform replicates into unique tags and titles
        if len(rep_tags) == 0:  # Replicates need special work after files are examined, so just stub.
            return (tag, live_group)
        # Inclusion of rep_tags occurs after files have been examined.
        live_group["groups"] = {}
        rep_title_mask = group_defs.get("title_mask","Replicate_{replicate_number}")
        for rep_tag in rep_tags:
            rep_title = rep_title_mask
            if "combined_title" in group_defs and rep_tag in ["pool","combined"]:
                rep_title = group_defs["combined_title"]
            elif rep_title_mask.find('{replicate}') != -1:
                rep_title = rep_title_mask.replace('{replicate}',rep_tag)
            elif rep_title_mask.find('{replicate_number}') != -1:
                if rep_tag in ["pool","combined"]:
                    rep_title = rep_title_mask.replace('{replicate_number}',"0")
                else:
                    rep_no = int(rep_tag[3:]) # tag might be rep01 but we want replicate 1
                    rep_title = rep_title_mask.replace('{replicate_number}',str(rep_no))
            live_group["groups"][rep_tag] = { "title": rep_title, "tag": rep_tag }
        live_group["preferred_order"] = "sorted"

    elif title in ["Biosample", "Targets", "Assay", EXP_GROUP ]: # Single subGroup at experiment level.  No order
        groups = group_defs.get("groups",{})
        assert(len(groups) == 1)
        for (group_key,group) in groups.items():
            mask = group.get("title_mask")
            if mask is not None:
                term = convert_mask(mask,dataset)
                if not term.startswith('Unknown '):
                    term_tag = sanitize_tag(term)
                    term_title = term
                    live_group["groups"] = {}
                    live_group["groups"][term_tag] = { "title": term_title, "tag": term_tag }
                    mask = group.get("url_mask")
                    if mask is not None:
                        term = convert_mask(mask,dataset)
                        live_group["groups"][term_tag]["url"] = term
        live_group["preferred_order"] = "sorted"
        # No tag order since only one

    # simple swapping tag and title and creating subgroups set with order
    else: # "Views", "Replicates", etc:
        # if there are subgroups, they can be handled by recursion
        if "groups" in group_defs:
            live_group["groups"]  = {}
            groups = group_defs["groups"]
            group_order = group_defs.get("group_order")
            preferred_order = []  # have to create preferred order based upon tags, not titles
            if group_order is None or not isinstance(group_order, list):
                group_order = sorted( groups.keys() )
                preferred_order = "sorted"
            tag_order = []
            for subgroup_title in group_order:
                subgroup = groups.get(subgroup_title,{})
                (subgroup_tag, subgroup) = generate_live_groups(composite,subgroup_title,subgroup,dataset) #recursive
                subgroup["tag"] = subgroup_tag
                if isinstance(preferred_order,list):
                    preferred_order.append(subgroup_tag)
                if title == "Views":
                    assert(subgroup_title != subgroup_tag)
                    handle_negateValues(subgroup, subgroup, dataset, composite)
                live_group["groups"][subgroup_tag] = subgroup
                tag_order.append(subgroup_tag)
            #assert(len(live_group["groups"]) == len(groups))
            if len(live_group['groups']) != len(groups):
                log.warn("len(live_group['groups']):%d != len(groups):%d" % \
                                                    (len(live_group['groups']), len(groups)))
                log.debug(json.dumps(live_group,indent=4))
            live_group["group_order"] = tag_order
            live_group["preferred_order"] = preferred_order

    return (tag, live_group)

def insert_live_group(live_groups,new_tag,new_group):
    '''Inserts new group into a set of live groups during composite remodelling.'''
    old_groups = live_groups.get("groups",{})
    preferred_order = live_groups.get("preferred_order") # Note: all cases where group is dynamically added should be in sort order!
    if preferred_order is None or not isinstance(preferred_order,list):
        old_groups[new_tag] = new_group
        live_groups["groups"] = old_groups
        #log.debug("Added %s to %s in sort order" % (new_tag,live_groups.get("tag","a group")))
        return live_groups

    # well we are going to have to generate s new order
    new_order = []
    old_order = live_groups.get("group_order",[])
    if old_order is None:
        old_order = sorted( old_groups.keys() )
    for preferred_tag in preferred_order:
        if preferred_tag == new_tag:
            new_order.append(new_tag)
        elif preferred_tag in old_order:
            new_order.append(preferred_tag)

    old_groups[new_tag] = new_group
    live_groups["groups"] = old_groups
    #log.debug("Added %s to %s in preferred order" % (new_tag,live_groups.get("tag","a group")))
    return live_groups

def biosamples_for_file(a_file,dataset):
    '''Returns a dict of biosamples for file.'''
    biosamples = {}
    replicates = dataset.get("replicates")
    if replicates is None:
        return[]

    for bio_rep in a_file.get("biological_replicates",[]):
        for replicate in replicates:
            if replicate.get("biological_replicate_number",-1) != bio_rep:
                continue
            biosample = replicate.get("library",{}).get("biosample",{})
            if not biosample:
                continue
            biosamples[biosample["accession"]] = biosample
            break  # If multiple techical replicates then the one should do

    return biosamples

def acc_composite_extend_with_tracks(composite, vis_defs, dataset, assembly, host=None):
    '''Extends live experiment composite object with track definitions'''
    tracks = []
    rep_techs = {}
    files = []
    ucsc_assembly = _ASSEMBLY_MAPPER.get(assembly, assembly)

    # first time through just to get rep_tech
    group_order = composite["view"].get("group_order",[])
    for view_tag in group_order:
        view = composite["view"]["groups"][view_tag]
        output_types = view.get("output_type",[])
        file_format_types = view.get("file_format_type",[])
        file_format = view["type"].split()[0]
        if file_format == "bigBed" and "scoreFilter" in view:
            view["type"] = "bigBed 6 +" # be more discriminating as to what bigBeds are 6 + ?  Just rely on scoreFilter
        #log.debug("%d files looking for type %s" % (len(dataset["files"]),view["type"]))
        for a_file in dataset["files"]:
            if a_file['status'] not in VISIBLE_FILE_STATUSES:
                continue
            if file_format != a_file['file_format']:
                #log.debug("- file_format %s does not match %s" % (a_file['file_format'],file_format))
                continue
            if len(output_types) > 0 and a_file.get('output_type','unknown') not in output_types:
                #log.debug("- wrong output_type: %s != %s" % (a_file.get('output_type','unknown'),str(output_types)))
                continue
            if len(file_format_types) > 0 and a_file.get('file_format_type','unknown') not in file_format_types:
                #log.debug("- wrong file_format_type: %s != %s" % (a_file.get('file_format_type','unknown'),str(file_format_types)))
                continue
            if 'assembly' not in a_file or _ASSEMBLY_MAPPER.get(a_file['assembly'], a_file['assembly']) != ucsc_assembly:
                #if 'assembly' not in a_file:
                #    log.debug("- no assembly")
                #else:
                #    log.debug("- wrong assembly %s != %s" % (_ASSEMBLY_MAPPER.get(a_file['assembly'], a_file['assembly']), ucsc_assembly))
                continue
            if "rep_tech" not in a_file:
                rep_tech = rep_for_file(a_file)
                a_file["rep_tech"] = rep_tech
            else:
                rep_tech = a_file["rep_tech"]
            rep_techs[rep_tech] = rep_tech
            files.append(a_file)
    if len(files) == 0:
        log.warn("No visualizable files for %s %s" % (dataset["accession"],composite["vis_type"]))
        return None

    # convert rep_techs to simple reps
    rep_ix = 1
    rep_tags = []
    for rep_tech in sorted( rep_techs.keys() ): # ordered by a simple sort
        if rep_tech == "combined":
            rep_tag = "pool"
        else:
            rep_tag = "rep%02d" % rep_ix
            rep_ix += 1
        rep_techs[rep_tech] = rep_tag
        rep_tags.append(rep_tag)

    # Now we can fill in "Replicate" subgroups with with "replicate"
    other_groups = vis_defs.get("other_groups",[]).get("groups",[])
    if "Replicates" in other_groups:
        group = other_groups["Replicates"]
        group_tag = group["tag"]
        subgroups = group["groups"]
        if "replicate" in subgroups:
            (repgroup_tag, repgroup) = generate_live_groups(composite,"replicate",subgroups["replicate"],dataset,rep_tags)
            # Now to hook them into the composite structure
            composite_rep_group = composite["groups"]["REP"]
            composite_rep_group["groups"] = repgroup.get("groups",{})
            composite_rep_group["group_order"] = repgroup.get("group_order",[])

    # second pass once all rep_techs are known
    if host is None:
        host = "https://www.encodeproject.org"
    for view_tag in composite["view"].get("group_order",[]):
        view = composite["view"]["groups"][view_tag]
        output_types = view.get("output_type",[])
        file_format_types = view.get("file_format_type",[])
        file_format = view["type"].split()[0]
        for a_file in files:
            #if file_format != a_file['file_format']:
            if a_file['file_format'] not in [ file_format, "bed" ]:
                continue
            if len(output_types) > 0 and a_file.get('output_type','unknown') not in output_types:
                continue
            if len(file_format_types) > 0 and a_file.get('file_format_type','unknown') not in file_format_types:
                continue
            rep_tech = a_file["rep_tech"]
            rep_tag = rep_techs[rep_tech]
            a_file["rep_tag"] = rep_tag

            if "tracks" not in view:
                view["tracks"] = []
            track = {}
            #track["name"] = "%s_%s" % (dataset['accession'][3:],a_file['accession'][3:]) # Trimming too cute?
            track["name"] = a_file['accession']
            track["type"] = view["type"]
            track["bigDataUrl"] = "%s?proxy=true" % a_file["href"]
            longLabel = vis_defs.get('file_defs',{}).get('longLabel')
            if longLabel is None:
                longLabel = "{assay_title} of {biosample_term_name} {output_type} {biological_replicate_number}"
            longLabel += " {experiment.accession} - {file.accession}" # Always add the accessions
            track["longLabel"] = sanitize_label( convert_mask(longLabel,dataset,a_file) )
            # Specialized addendum comments because subtle details are always getting in the way of elegance.
            addendum = ""
            submitted_name = a_file.get('submitted_file_name',"none")
            if "_tophat" in submitted_name:
                addendum = addendum + 'TopHat,'
            if a_file.get('assembly',assembly) == 'mm10-minimal':
                addendum = addendum + 'mm10-minimal,'
            if len(addendum) > 0:
                track["longLabel"] = track["longLabel"] + " (" + addendum[0:-1] + ")" # add mm10-minimal into the longLabel


            metadata_pairs = {}
            metadata_pairs['file&#32;download'] = '"<a href=\'%s%s\' title=\'Download this file from the ENCODE portal\'>%s</a>"' % (host,a_file["href"],a_file["accession"])
            lab_title = a_file.get("lab",dataset.get("lab",{})).get("title")
            if "replicate" in a_file:
                bio_rep = a_file["replicate"]["biological_replicate_number"]
                tech_rep = a_file["replicate"]["technical_replicate_number"]
                metadata_pairs['biological&#32;replicate'] = str(bio_rep)
                metadata_pairs['technical&#32;replicate'] = str(tech_rep)
            else:
                bio_rep = a_file.get('biological_replicates')
                if bio_rep and len(bio_rep) == 1:
                    metadata_pairs['biological&#32;replicate'] = str(bio_rep[0])
                tech_rep = a_file.get('technical_replicates')
                if tech_rep and len(tech_rep) == 1:
                    metadata_pairs['technical&#32;replicate'] = tech_rep[0].split('_')[1]

            # Expecting short label to change when making assay based composites
            shortLabel = vis_defs.get('file_defs',{}).get('shortLabel',"{replicate} {output_type_short_label}")
            track["shortLabel"] = sanitize_label( convert_mask(shortLabel,dataset,a_file) )

            # How about subgroups!
            membership = {}
            membership["view"] = view["tag"]
            view["tracks"].append( track )  # <==== This is how we connect them to the views
            for (group_tag,group) in composite["groups"].items():
                # "Replicates", "Biosample", "Targets", "Assay", ... member?
                group_title = group["title"]
                subgroups = group["groups"]
                if group_title == "Replicates":
                    # Must figure out membership
                    ### Generate rep_tag for track, then
                    subgroup = subgroups.get(rep_tag)
                    #if subgroup is None:
                    #    subgroup = { "tag": rep_tag, "title": rep_tag }
                    #    group["groups"][rep_tag] = subgroup
                    if subgroup is not None:
                        membership[group_tag] = rep_tag
                        if "tracks" not in subgroup:
                            subgroup["tracks"] = []
                        subgroup["tracks"].append( track )  # <==== also connected to replicate
                elif group_title in ["Biosample", "Targets", "Assay",EXP_GROUP]:
                    assert(len(subgroups) == 1)
                    #if len(subgroups) == 1:
                    for (subgroup_tag,subgroup) in subgroups.items():
                        membership[group_tag] = subgroup["tag"]
                        if "url" in subgroup:
                            metadata_pairs[group_title] = '"<a href=\'%s/%s/\' TARGET=\'_blank\' title=\'%s details at the ENCODE portal\'>%s</a>"' % (host,subgroup["url"],group_title,subgroup["title"])
                        elif group_title == "Biosample":
                            bs_value = sanitize_label( dataset.get("biosample_summary","") )
                            if len(bs_value) == 0:
                                bs_value = subgroup["title"]
                            biosamples = biosamples_for_file(a_file,dataset)
                            if len(biosamples) > 0:
                                for bs_acc in sorted( biosamples.keys() ):
                                    bs_value += " <a href=\'%s%s\' TARGET=\'_blank\' title=\'%s details at the ENCODE portal\'>%s</a>" % (host,biosamples[bs_acc]["@id"],group_title,bs_acc)
                            metadata_pairs[group_title] = '"%s"' % (bs_value)
                        else:
                            metadata_pairs[group_title] = '"%s"' % (subgroup["title"])
                else:
                    ### Help!
                    assert(group_tag == "Don't know this group!")

            track["membership"] = membership
            if len(metadata_pairs):
                track["metadata_pairs"] = metadata_pairs

            tracks.append(track)

    return tracks

def make_acc_composite(dataset, assembly, host=None, hide=False):
    '''Converts experiment composite static definitions to live composite object'''
    if dataset["status"] not in VISIBLE_DATASET_STATUSES:
        log.warn("%s can't be visualized because it's not unreleased status:%s." % (dataset["accession"],dataset["status"]))
        return {}
    vis_type = get_vis_type(dataset)
    vis_defs = lookup_vis_defs(vis_type)
    if vis_defs is None:
        log.warn("%s (vis_type: %s) has undiscoverable vis_defs." % (dataset["accession"],vis_type))
        return {}
    composite = {}
    #log.debug("%s has vis_type: %s." % (dataset["accession"],vis_type))
    composite["vis_type"] = vis_type
    composite["name"] = dataset["accession"]

    longLabel = vis_defs.get('longLabel','{assay_term_name} of {biosample_term_name} - {accession}')
    composite['longLabel'] = sanitize_label( convert_mask(longLabel,dataset) )
    shortLabel = vis_defs.get('shortLabel','{accession}')
    composite['shortLabel'] = sanitize_label( convert_mask(shortLabel,dataset) )
    if hide:
        composite["visibility"] = "hide"
    else:
        composite["visibility"] = vis_defs.get("visibility","full")
    composite['pennantIcon'] = find_pennent(dataset)
    add_living_color(composite, dataset)
    # views are always subGroup1
    composite["view"] = {}
    title_to_tag = {}
    if "Views" in vis_defs:
        ( tag, views ) = generate_live_groups(composite,"Views",vis_defs["Views"],dataset)
        composite[tag] = views
        title_to_tag["Views"] = tag

    if "other_groups" in vis_defs:
        groups = vis_defs["other_groups"].get("groups",{})
        new_dimensions = {}
        new_filters = {}
        composite["group_order"] = []
        composite["groups"] = {} # subgroups are defined by groups and group_order directly off of composite
        group_order = vis_defs["other_groups"].get("group_order")
        preferred_order = []  # have to create preferred order based upon tags, not titles
        if group_order is None or not isinstance(group_order,list):
            group_order = sorted( groups.keys() )
            preferred_order = "sorted"
        for subgroup_title in group_order: # Replicates, Targets, Biosamples
            if subgroup_title not in groups:
                continue
            assert(subgroup_title in SUPPORTED_SUBGROUPS)
            (subgroup_tag, subgroup) = generate_live_groups(composite,subgroup_title,groups[subgroup_title],dataset)
            if isinstance(preferred_order,list):
                preferred_order.append(subgroup_tag)  # "Targets" will get in, even if there are no targets in dataset
            if "groups" in subgroup and len(subgroup["groups"]) > 0: # This means "Targets" may not get in
                title_to_tag[subgroup_title] = subgroup_tag
                #subgroup["subgroup_ix"] = subgroup_ix # Only matters when printing out and remodelling requires not setting now
                composite["groups"][subgroup_tag] = subgroup
                composite["group_order"].append(subgroup_tag)
            if "dimensions" in vis_defs["other_groups"]: # "Targets" dimension will be included, whether there is a target group or not
                dimension = vis_defs["other_groups"]["dimensions"].get(subgroup_title)
                if dimension is not None:
                    new_dimensions[dimension] = subgroup_tag
                    if "filterComposite" in vis_defs["other_groups"]:
                        filterfish = vis_defs["other_groups"]["filterComposite"].get(subgroup_title)
                        if filterfish is not None:
                            new_filters[dimension] = filterfish
        composite["preferred_order"] = preferred_order
        if len(new_dimensions) > 0:
            composite["dimensions"] = new_dimensions
        if len(new_filters) > 0:
            composite["filterComposite"] = new_filters
        if "dimensionAchecked" in vis_defs["other_groups"]:
            composite["dimensionAchecked"] = vis_defs["other_groups"]["dimensionAchecked"]

    if "sortOrder" in vis_defs:
        sort_order = []
        for title in vis_defs["sortOrder"]:
            if title in title_to_tag:
                sort_order.append(title_to_tag[title])
        composite["sortOrder"] = sort_order

    tracks = acc_composite_extend_with_tracks(composite, vis_defs, dataset, assembly, host=host)
    if tracks is None or len(tracks) == 0:
        # Already warned about files log.debug("No tracks for %s" % dataset["accession"])
        return {}
    composite["tracks"] = tracks
    return composite

def remodel_acc_to_set_composites(acc_composites,hide_after=None):
    '''Given a set of (search result) acc based composites, remodel them to set based composites.'''
    if acc_composites is None or len(acc_composites) == 0:
        return {}

    set_composites = {}

    for acc in sorted( acc_composites.keys() ):
        acc_composite = acc_composites[acc]
        if acc_composite is None or len(acc_composite) == 0: # wounded composite can be dropped or added for evidence
            #log.debug("Found empty acc_composite for %s" % (acc))
            set_composites[acc] = {}
            continue

        # Only show the first n datasets
        if hide_after != None:
            if hide_after <= 0:
                for track in acc_composite.get("tracks",{}):
                    track["checked"] = "off"
            else:
                hide_after -= 1

        # color must move to tracks becuse it is likely biosample based and we are likely mixing biosample exps
        acc_color = acc_composite.get("color")
        acc_altColor = acc_composite.get("altColor")
        acc_view_groups = acc_composite.get("view",{}).get("groups",{})
        for (view_tag,acc_view) in acc_view_groups.items():
            acc_view_color = acc_view.get("color",acc_color) # color may be at view level if negateValues os on
            acc_view_altColor = acc_view.get("altColor",acc_altColor)
            if acc_view_color is None and acc_view_altColor is None:
                continue
            for track in acc_view.get("tracks",[]):
                if "color" not in track.keys():
                    if acc_view_color is not None:
                        track["color"] = acc_view_color
                    if acc_view_altColor is not None:
                        track["altColor"] = acc_view_altColor

        # If set_composite of this vis_type doesn't exist, create it
        vis_type = acc_composite["vis_type"]
        vis_defs = lookup_vis_defs(vis_type)
        assert(vis_type is not None)
        if vis_type not in set_composites.keys():  # First one so just drop in place
            #log.debug("Remodelling %s into %s composite" % (acc_composite.get("name"," a composite"),vis_type))
            set_composite = acc_composite # Don't bother with deep copy... we aren't needing the acc_composites any more
            set_defs = vis_defs.get("assay_composite",{})
            set_composite["name"] = vis_type.lower()  # is there something more elegant?
            for tag in ["longLabel","shortLabel","visibility"]:
                if tag in set_defs:
                    set_composite[tag] = set_defs[tag] # Not expecting any token substitutions!!!
            set_composite['html'] = vis_type
            set_composites[vis_type] = set_composite

        else: # Adding an acc_composite to an existing set_composite
            #log.debug("Adding %s into %s composite" % (acc_composite.get("name"," a composite"),vis_type))
            set_composite = set_composites[vis_type]
            set_composite['composite_type'] = 'set'

            if set_composite.get("project","unknown") != "NHGRI":
                acc_pennant = acc_composite["pennantIcon"]
                set_pennant = set_composite["pennantIcon"]
                if acc_pennant != set_pennant:
                    set_composite["project"] = "NHGRI"
                    set_composite["pennantIcon"] = PENNANTS["NHGRI"]

            # combine views
            set_views = set_composite.get("view",[])
            acc_views = acc_composite.get("view",{})
            for view_tag in acc_views["group_order"]:
                acc_view = acc_views["groups"][view_tag]
                if view_tag not in set_views["groups"].keys():  # Should never happen
                    #log.debug("Surprise: view %s not found before" % view_tag)
                    insert_live_group(set_views,view_tag,acc_view)
                else: # View is already defined but tracks need to be appended.
                    set_view = set_views["groups"][view_tag]
                    if "tracks" not in set_view:
                        set_view["tracks"] = acc_view.get("tracks",[])
                    else:
                        set_view["tracks"].extend(acc_view.get("tracks",[]))

            # All tracks in one set: not needed.

            # Combine subgroups:
            for group_tag in acc_composite["group_order"]:
                acc_group = acc_composite["groups"][group_tag]
                if group_tag not in set_composite["groups"].keys(): # Should never happen
                    #log.debug("Surprise: group %s not found before" % group_tag)
                    insert_live_group(set_composite,group_tag,acc_group)
                else: # Need to handle subgroups which definitely may not be there.
                    set_group = set_composite["groups"].get(group_tag,{})
                    acc_subgroups = acc_group.get("groups",{})
                    acc_subgroup_order = acc_group.get("group_order")
                    for subgroup_tag in acc_subgroups.keys():
                        if subgroup_tag not in set_group.get("groups",{}).keys():
                            insert_live_group(set_group,subgroup_tag,acc_subgroups[subgroup_tag]) # Adding biosamples, targets, and reps

            # dimensions and filterComposite should not need any extra care: they get dynamically scaled down during printing
            #log.debug("       Added.")

    return set_composites

def ucsc_trackDb_composite_blob(composite,title):
    '''Given an in-memory composite object, prints a single UCSC trackDb.txt composite structure'''
    if composite is None or len(composite) == 0:
        return "# Empty composite for %s.  It cannot be visualized at this time.\n" % title
    # TODO provide more detail about different possible reasons (should already be in errorlog)

    blob = ""
    # First the composite structure
    blob += "track %s\n" % composite["name"]
    blob += "compositeTrack on\n"
    blob += "type bed 3\n"
    for var in COMPOSITE_SETTINGS:
        val = composite.get(var)
        if val:
            blob += "%s %s\n" % (var, val)
    views = composite.get("view",[])
    if len(views) > 0:
        blob += "subGroup1 view %s" % views["title"]
        for view_tag in views["group_order"]:
            view_title = views["groups"][view_tag]["title"]
            blob += " %s=%s" % (view_tag,sanitize_title(view_title))
        blob += '\n'
    dimA_checked = composite.get("dimensionAchecked","all")
    dimA_tag = ""
    if dimA_checked == "first": # All will leave dimA_tag and dimA_checked empty, thus defaulting to all on
        dimA_tag = composite.get("dimensions",{}).get("dimA","")
    dimA_checked = None
    subgroup_ix = 2
    for group_tag in composite["group_order"]:
        group = composite["groups"][group_tag]
        blob += "subGroup%d %s %s" % (subgroup_ix, group_tag, sanitize_title(group["title"]))
        subgroup_ix += 1
        subgroup_order = None # group.get("group_order")
        if subgroup_order is None or not isinstance(subgroup_order,list):
            subgroup_order = sorted( group["groups"].keys() )
        for subgroup_tag in subgroup_order:
            subgroup_title = group["groups"][subgroup_tag]["title"]
            blob += " %s=%s" % (subgroup_tag,sanitize_title(subgroup_title))
            if group_tag == dimA_tag and dimA_checked is None:
                dimA_checked = subgroup_tag

        blob += '\n'
    # sortOrder
    sort_order = composite.get("sortOrder")
    if sort_order:
        blob += "sortOrder"
        for sort_tag in sort_order:
            if title.startswith("ENCSR") and sort_tag == "EXP": # Single exp composites do not need to sort on EMP
                continue
            blob += " %s=+" % sort_tag
        blob += '\n'
    # dimensions
    actual_group_tags = [ "view" ] # Not all groups will be used in composite, depending upon subgroup content
    dimensions = composite.get("dimensions",{})
    if dimensions:
        pairs = ""
        XY_skipped = []
        XY_added = []
        for dim_tag in sorted( dimensions.keys() ):
            group = composite["groups"].get(dimensions[dim_tag])
            if group is None: # e.g. "Targets" may not exist
                continue
            if dimensions[dim_tag] != "REP":
                if len(group.get("groups",{})) <= 1:
                    if dim_tag[-1] in ['X','Y']:
                        XY_skipped.append(dim_tag)
                    continue
                elif dim_tag[-1] in ['X','Y']:
                    XY_added.append(dim_tag)
            pairs += " %s=%s" % (dim_tag, dimensions[dim_tag])
            actual_group_tags.append(dimensions[dim_tag])
        # Getting too fancy for our own good: If one XY dimension has more than one member then we must add both X and Y
        if len(XY_skipped) > 0 and len(XY_added) > 0:
            for dim_tag in XY_skipped:
                pairs += " %s=%s" % (dim_tag, dimensions[dim_tag])
                actual_group_tags.append(dimensions[dim_tag])
        if len(pairs) > 0:
            blob += "dimensions%s\n" % pairs
    # filterComposite
    filter_composite = composite.get("filterComposite")
    if filter_composite:
        filterfish = ""
        for filter_tag in sorted( filter_composite.keys() ):
            group = composite["groups"].get(filter_composite[filter_tag])
            if group is None or len(group.get("groups",{})) <= 1: # e.g. "Targets" may not exist
                continue
            filterfish += " %s" % filter_tag
            if filter_composite[filter_tag] == "one":
                filterfish += "=one"
        if len(filterfish) > 0:
            blob += 'filterComposite%s\n' % filterfish
    elif dimA_checked is not None:
        blob += 'dimensionAchecked %s\n' % dimA_checked
    blob += '\n'

    # Now cycle through views
    for view_tag in views["group_order"]:
        view = views["groups"][view_tag]
        tracks = view.get("tracks",[])
        if len(tracks) == 0:
            continue
        blob += "    track %s_%s_view\n" % (composite["name"],view["tag"])
        blob += "    parent %s on\n" % composite["name"]
        blob += "    view %s\n" % view["tag"]
        for var in VIEW_SETTINGS:
            val = view.get(var)
            if val:
                blob += "    %s %s\n" % (var, val)
        blob += '\n'

        # Now cycle through tracks in view
        for track in tracks:
            blob += "        track %s\n" % (track["name"])
            blob += "        parent %s_%s_view" % (composite["name"],view["tag"])
            dimA_subgroup = track.get("membership",{}).get(dimA_tag)
            if dimA_subgroup is not None and dimA_subgroup != dimA_checked:
                blob += " off\n"
            else:
                blob += " %s\n" % track.get("checked","on") # Can set individual tracks off. Used when remodelling
            if "type" not in track:
                blob += "        type %s\n" % (view["type"])
            for var in TRACK_SETTINGS:
                val = track.get(var)
                if val:
                    blob += "        %s %s\n" % (var, val)
            # Now membership
            membership = track.get("membership")
            if membership:
                blob += "        subGroups"
                for member_tag in sorted( membership ):
                    #if member_tag in actual_group_tags: # TODO: remove when it is proved to be not needed.
                    blob += " %s=%s" % (member_tag,membership[member_tag])
                blob += '\n'
            # metadata line?
            metadata_pairs = track.get("metadata_pairs")
            if metadata_pairs is not None:
                metadata_line = ""
                for meta_tag in sorted( metadata_pairs.keys() ):
                    metadata_line += ' %s=%s' % (meta_tag.lower(),metadata_pairs[meta_tag])
                if len(metadata_line) > 0:
                    blob += "        metadata%s\n" % metadata_line

            blob += '\n'
    blob += '\n'
    return blob

def find_or_make_acc_composite(request, assembly, acc, dataset=None, hide=False, regen=False):

    ### local test: bigBed: curl http://localhost:8000/experiments/ENCSR000DZQ/@@hub/hg19/trackDb.txt
    ###             bigWig: curl http://localhost:8000/experiments/ENCSR000ADH/@@hub/mm9/trackDb.txt
    ### CHIP: https://4217-trackhub-spa-ab9cd63-tdreszer.demo.encodedcc.org/experiments/ENCSR645BCH/@@hub/GRCh38/trackDb.txt
    ### LRNA: curl https://4217-trackhub-spa-ab9cd63-tdreszer.demo.encodedcc.org/experiments/ENCSR000AAA/@@hub/GRCh38/trackDb.txt

    # USE ES CACHE
    USE_CACHE = True # TODO: set to True when ready to try Bek's cache priming solution.

    acc_composite = None
    es_key = acc + "_" + assembly
    found_or_made = "found"
    if USE_CACHE:
        if not regen:
            regen = (request.url.find("regenvis") > -1) # @@hub/GRCh38/regenvis/trackDb.txt  regenvis/GRCh38 causes and error

        if not regen: # Find composite?
            acc_composite = get_from_es(request,es_key)

    if acc_composite is None:
        request_dataset = (dataset is None)
        if request_dataset:
            dataset = request.embed("/datasets/" + acc + '/', as_user=True)
            #log.debug("find_or_make_acc_composite len(results) = %d   %.3f secs" % (len(results),(time.time() - PROFILE_START_TIME)))

        acc_composite = make_acc_composite(dataset, assembly, host=request.host_url, hide=hide)
        if USE_CACHE:
            add_to_es(request,es_key,acc_composite)
        #if not regen:
        #    log.info("made acc_composite %s_%s" % (acc, assembly))
        found_or_made = "made"

        if request_dataset: # Manage meomory
            del dataset

    return (found_or_made, acc_composite)


def generate_trackDb(request, dataset, assembly, hide=False, regen=False):

    acc = dataset['accession']
    ucsc_assembly = _ASSEMBLY_MAPPER.get(assembly, assembly)
    (found_or_made, acc_composite) = find_or_make_acc_composite(request, ucsc_assembly, \
                                            dataset["accession"], dataset, hide=hide, regen=regen)
    vis_type = acc_composite.get("vis_type",get_vis_type(dataset))
    log.debug("%s composite %s_%s %s %.3f" % (found_or_made,dataset['accession'],ucsc_assembly, \
                                                    vis_type,(time.time() - PROFILE_START_TIME)))
    #del dataset
    json_out = (request.url.find("jsonout") > -1) # @@hub/GRCh38/jsonout/trackDb.txt  regenvis/GRCh38 causes and error
    if json_out:
        return json.dumps(acc_composite,indent=4,sort_keys=True)
    return ucsc_trackDb_composite_blob(acc_composite,acc)

def make_set_key(param_list,assembly):
    '''Returns a key for es cache for a set of search parameters'''
    es_set_key = "assembly=%s" % assembly
    for param_key in sorted( param_list.keys() ):  # Most important to sort, to ensure 2 identical (but different order) searches) resolve
        params = sorted( param_list[param_key] )
        es_set_key += ',,' + param_key + '=' + params[0]
        if len(params) > 1:
            for param in params[1:]:
                es_set_key += '|' + str(param)
    return es_set_key

def generate_batch_trackDb(request, hide=False, regen=False):

    ### local test: RNA-seq: curl https://4217-trackhub-spa-ab9cd63-tdreszer.demo.encodedcc.org/batch_hub/type=Experiment,,assay_title=RNA-seq,,award.rfa=ENCODE3,,status=released,,assembly=GRCh38,,replicates.library.biosample.biosample_type=induced+pluripotent+stem+cell+line/GRCh38/trackDb.txt

    USE_CACHE = True # TODO: set to True when ready to try Bek's cache priming solution.
    CACHE_SETS = False  # NO CACHING OF set_composites!!!

    # Special logic to force remaking of trackDb
    if not regen:
        regen = (request.url.find("regenvis") > -1) # ...&assembly=hg19&regenvis/hg19/trackDb.txt  regenvis=1 causes an error
    find_or_make = "find or make"
    if not regen: # Find composite?
        find_or_make = "make"

    assembly = str(request.matchdict['assembly'])
    log.debug("Request for %s trackDb begins   %.3f secs" % (assembly,(time.time() - PROFILE_START_TIME)))
    param_list = parse_qs(request.matchdict['search_params'].replace(',,', '&'))

    set_composites = None
    # Create an appropriate cache key
    if USE_CACHE and CACHE_SETS:
        set_composites = None
        es_set_key = make_set_key(param_list,assembly)

        # Find it?
        if not regen: # Force regeneration?
            set_composites = get_from_es(request,es_set_key)
            if set_composites is not None:
                log.debug("Found with key %s   %.3f secs" % (es_set_key,(time.time() - PROFILE_START_TIME)))

    if set_composites is None:

        # Have to make it.
        assemblies = ASSEMBLY_MAPPINGS.get(assembly,[assembly])
        params = {
            'files.file_format': BIGBED_FILE_TYPES + BIGWIG_FILE_TYPES,
        }
        params.update(param_list)
        params.update({
            'assembly': assemblies,
            'limit': ['all'],
        })
        if not USE_CACHE:
            params['frame'] = ['embedded'] # Note: Poor memory usage, since acc_composites should all be in cache

        view = 'search'
        if 'region' in param_list:
            view = 'region-search'
        path = '/%s/?%s' % (view, urlencode(params, True))
        results = request.embed(path, as_user=True)['@graph']
        if not USE_CACHE:
            log.debug("len(results) = %d   %.3f secs" % (len(results),(time.time() - PROFILE_START_TIME)))
        else:
            # Note: better memory usage to get acc array from non-embedded results, since acc_composites should be in cache
            accs = [result['accession'] for result in results]
            del results

        found = 0
        made = 0
        if USE_CACHE and not regen:
            es_keys = [acc + "_" + assembly for acc in accs]
            acc_composites = search_es(request, es_keys)
            found = len(acc_composites)
            
        if found == 0: # if 0 were found in cache try generating (for pre-primed-cache access)
            acc_composites = {}
            if not USE_CACHE:
                for dataset in results:          # Note: Poor memory usage, since acc_composites should all be in cache
                    acc = dataset['accession']
                    (found_or_made, acc_composite) = find_or_make_acc_composite(request, assembly, acc, dataset, hide=hide, regen=True)
                    made += 1
                    acc_composites[acc] = acc_composite
            else:
                for acc in accs:
                    (found_or_made, acc_composite) = find_or_make_acc_composite(request, assembly, acc, None, hide=hide, regen=regen)
                    if found_or_made == "made":
                        made += 1
                        #log.debug("%s composite %s" % (found_or_made,acc))
                    else:
                        found += 1
                    acc_composites[acc] = acc_composite

        set_composites = remodel_acc_to_set_composites(acc_composites, hide_after=100)
        if USE_CACHE and CACHE_SETS:
            add_to_es(request,es_set_key,set_composites)
        log.debug("%d acc_composites => %d set_composites (%s generated, %d found)   %.3f secs" % \
            ((made + found),len(set_composites),made,found,(time.time() - PROFILE_START_TIME)))

    json_out = (request.url.find("jsonout") > -1) # ...&assembly=hg19&jsonout/hg19/trackDb.txt
    if json_out:
        return json.dumps(set_composites,indent=4,sort_keys=True)

    blob = ""
    for composite_tag in sorted( set_composites.keys() ):
        blob += ucsc_trackDb_composite_blob(set_composites[composite_tag],composite_tag)
    log.debug("Length of trackDb %d   %.3f secs" % (len(blob),(time.time() - PROFILE_START_TIME)))

    return blob

# TODO: uncomment when ready to try Bek's cache priming solution.
@subscriber(AfterIndexedExperimentsAndDatasets)
def prime_vis_es_cache(event):
    request = event.request
    uuids = event.object
    
    # NOTE: log.warn (not debug) to be seen, since this log is NOT in this module's scope
    #log.warn("Starting prime_vis_es_cache")

    visualizabe_types = set(VISIBLE_DATASET_TYPES)
    count = 0
    for uuid in uuids:
        dataset = request.embed(uuid)
        # Try to limit the sets we are interested in
        if dataset.get('status','none') not in VISIBLE_DATASET_STATUSES:
            continue
        if visualizabe_types.isdisjoint(dataset['@type']):
            continue
        acc = dataset['accession']
        assemblies = dataset.get('assembly',[])
        for assembly in assemblies:
            ucsc_assembly = _ASSEMBLY_MAPPER.get(assembly, assembly)
            (found_or_made, acc_composite) = find_or_make_acc_composite(request, ucsc_assembly, \
                                                                        acc, dataset, regen=True)
            if acc_composite:
                count += 1
                log.warn("primed vis_es_cache with acc_composite %s_%s '%s'" % \
                                            (acc,ucsc_assembly,acc_composite.get('vis_type','')))
            else:
                log.warn("prime_vis_es_cache for %s_%s unvisualizable '%s'" % \
                                            (acc,ucsc_assembly,get_vis_type(dataset)))
    if count == 0:
        log.warn("prime_vis_es_cache made %d acc_composites" % (count))

def render(data):
    arr = []
    for i in range(len(data)):
        temp = list(data.popitem())
        str1 = ' '.join(temp)
        arr.append(str1)
    return arr


def get_genome_txt(assembly):
    # UCSC shim
    ucsc_assembly = _ASSEMBLY_MAPPER.get(assembly, assembly)
    genome = OrderedDict([
        ('trackDb', ucsc_assembly + '/trackDb.txt'),
        ('genome', ucsc_assembly)
    ])
    return render(genome)

def get_genomes_txt(assemblies):
    blob = ''
    ucsc_assemblies = set()
    for assembly in assemblies:
        ucsc_assemblies.add(_ASSEMBLY_MAPPER.get(assembly, assembly))
    for ucsc_assembly in ucsc_assemblies:
        if blob == '':
            blob = NEWLINE.join(get_genome_txt(ucsc_assembly))
        else:
            blob += 2 * NEWLINE + NEWLINE.join(get_genome_txt(ucsc_assembly))
    return blob


def get_hub(label,comment=None,name=None):
    if name is None:
        name = sanitize_name( label.split()[0] )
    if comment is None:
        comment = "Generated by the ENCODE portal"
    hub = OrderedDict([
        ('email', 'encode-help@lists.stanford.edu'),
        ('genomesFile', 'genomes.txt'),
        ('longLabel', 'ENCODE Data Coordination Center Data Hub'),
        ('shortLabel', 'Hub (' + label + ')'),
        ('hub', 'ENCODE_DCC_' + name ),
        ('#', comment )
    ])
    return render(hub)

def generate_html(context, request):
    ''' Generates and returns HTML for the track hub'''

    # First determine if single dataset or collection
    #log.debug("HTML request: %s" % request.url)

    html_requested = request.url.split('/')[-1].split('.')[0]
    if html_requested.startswith('ENCSR'):
        embedded = request.embed(request.resource_path(context))
        acc = embedded['accession']
        log.debug("generate_html for %s   %.3f secs" % (acc,(time.time() - PROFILE_START_TIME)))
        assert( html_requested == acc)

        vis_type = get_vis_type(embedded)
        vis_defs = lookup_vis_defs(vis_type)
        longLabel = vis_defs.get('longLabel','{assay_term_name} of {biosample_term_name} - {accession}')
        longLabel = sanitize_label( convert_mask(longLabel,embedded) )

        link = request.host_url + '/experiments/' + acc + '/'
        acc_link = '<a href={link}>{accession}<a>'.format(link=link, accession=acc)
        if longLabel.find(acc) != -1:
            longLabel = longLabel.replace(acc,acc_link)
        else:
            longLabel += " - " + acc_link
        page = '<h2>%s</h2>' % longLabel

    else: # collection
        vis_type = html_requested
        vis_defs = lookup_vis_defs(vis_type)
        longLabel = vis_defs.get('assay_composite',{}).get('longLabel',"Unknown collection of experiments")
        page = '<h2>%s</h2>' % longLabel

        # TO IMPROVE: limit the search url to this assay only.  Not easy since vis_def is not 1:1 with assay
        try:
            param_list = parse_qs(request.matchdict['search_params'].replace(',,', '&'))
            search_url = '%s/search/?%s' % (request.host_url,urlencode(param_list, True))
            #search_url = (request.url).split('@@hub')[0]
            search_link = '<a href=%s>Original search<a><BR>' % search_url
            page += search_link
        except:
            pass

    # TODO: Extend page with assay specific details
    details = vis_defs.get("html_detail")
    if details is not None:
        page += details

    return page # data_description + header + file_table


def generate_batch_hubs(context, request):
    '''search for the input params and return the trackhub'''
    global PROFILE_START_TIME
    PROFILE_START_TIME = time.time()

    results = {}
    txt = request.matchdict['txt']

    if len(request.matchdict) == 3:

        # Should generate a HTML page for requests other than trackDb.txt
        if txt != TRACKDB_TXT:
            data_policy = '<br /><a href="http://encodeproject.org/ENCODE/terms.html">ENCODE data use policy</p>'
            return generate_html(context, request) + data_policy

        return generate_batch_trackDb(request)

    elif txt == HUB_TXT:
        terms = request.matchdict['search_params'].replace(',,', '&')
        pairs = terms.split('&')
        label = "search:"
        for pair in sorted( pairs ):
            (var,val) = pair.split('=')
            if var not in ["type","assembly","status","limit"]:
                label += " %s" % val.replace('+',' ')
        return NEWLINE.join(get_hub(label,request.url))
    elif txt == GENOMES_TXT:
        param_list = parse_qs(request.matchdict['search_params'].replace(',,', '&'))

        view = 'search'
        if 'region' in param_list:
            view = 'region-search'
        path = '/%s/?%s' % (view, urlencode(param_list, True))
        results = request.embed(path, as_user=True)
        #log.debug("generate_batch(genomes) len(results) = %d   %.3f secs" % (len(results),(time.time() - PROFILE_START_TIME)))
        g_text = ''
        if 'assembly' in param_list:
            g_text = get_genomes_txt(param_list.get('assembly'))
        else:
            for facet in results['facets']:
                if facet['field'] == 'assembly':
                    assemblies = []
                    for term in facet['terms']:
                        if term['doc_count'] != 0:
                            assemblies.append(term['key'])
                    if len(assemblies) > 0:
                        g_text = get_genomes_txt(assemblies)
        return g_text


@view_config(name='hub', context=Item, request_method='GET', permission='view')
def hub(context, request):
    ''' Creates trackhub on fly for a given experiment '''
    global PROFILE_START_TIME
    PROFILE_START_TIME = time.time()

    url_ret = (request.url).split('@@hub')
    embedded = request.embed(request.resource_path(context))

    if url_ret[1][1:] == HUB_TXT:
        typeof = embedded.get("assay_title")
        if typeof is None:
            typeof = embedded["@id"].split('/')[1]

        label = "%s %s" % (typeof, embedded['accession'])
        name = sanitize_name( label )
        return Response(
            NEWLINE.join(get_hub(label,request.url, name )),
            content_type='text/plain'
        )
    elif url_ret[1][1:] == GENOMES_TXT:
        assemblies = ''
        if 'assembly' in embedded:
            assemblies = embedded['assembly']

        g_text = get_genomes_txt(assemblies)
        return Response(g_text, content_type='text/plain')

    elif url_ret[1][1:].endswith(TRACKDB_TXT):
        trackDb = generate_trackDb(request, embedded, url_ret[1][1:].split('/')[0])
        return Response(trackDb, content_type='text/plain')
    else:
        data_policy = '<br /><a href="http://encodeproject.org/ENCODE/terms.html">ENCODE data use policy</p>'
        return Response(generate_html(context, request) + data_policy, content_type='text/html')


@view_config(route_name='batch_hub')
@view_config(route_name='batch_hub:trackdb')
def batch_hub(context, request):
    ''' View for batch track hubs '''
    return Response(generate_batch_hubs(context, request), content_type='text/plain')
