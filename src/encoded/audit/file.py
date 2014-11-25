from ..auditor import (
    AuditFailure,
    audit_checker,
)
from pyramid.traversal import find_root

current_statuses = ['released', 'in progress']
not_current_statuses = ['revoked', 'obsolete', 'deleted']
raw_data_formats = [
    'fastq',
    'csfasta',
    'csqual',
    'rcc',
    'idat',
    'CEL',
    ]


@audit_checker('file')
def audit_file_platform(value, system):
    '''
    A raw data file should have a platform specified.
    Should be in the schema.
    '''

    if value['status'] in ['deleted', 'replaced']:
        return

    if value['format'] not in raw_data_formats:
        return

    if 'platform' not in value:
        detail = 'Raw data file {} missing platform information'.format(value['accession'])
        raise AuditFailure('missing platform', detail, level='STANDARDS_FAILURE')


@audit_checker('file')
def audit_file_flowcells(value, system):
    '''
    A fastq file could have its flowcell details.
    '''

    if value['status'] in ['deleted', 'replaced']:
        return

    if value['format'] not in ['fastq']:
        return

    if 'flowcell_details' not in value or (value['flowcell_details'] == {}):
        detail = 'Fastq file {} missing flowcell details'.format(value['accession'])
        raise AuditFailure('missing platform', detail, level='WARNING')


@audit_checker('file')
def audit_paired_with(value, system):
    '''
    A file with a paired_end needs a paired_with.
    Should be handled in the schema.
    A paired_with should be the same replicate
    '''

    if value['status'] in ['deleted', 'replaced']:
        return

    if 'paired_end' not in value:
        return

    if 'paired_with' not in value:
        detail = '{} is pair {} and missing paired_with'.format(value['accession'],
                                                                value['paired_end'])
        raise AuditFailure('missing paired_with', detail, level='ERROR')

    # Would love to then check to see if the files shared the same replicate


@audit_checker('file')
def audit_file_size(value, system):

    if value['status'] in ['deleted', 'replaced', 'uploading']:
        return

    if 'file_size' not in value:
        detail = '{} missing file_size'.format(value['accession'])
        raise AuditFailure('missing file_size', detail, level='STANDARDS_FAILURE')


@audit_checker('file')
def audit_file_status(value, system):

    file_status = value.get('status')

    if file_status == 'deleted':
        return

    if 'dataset' not in value:
        detail = 'missing dataset'
        raise AuditFailure('missing dataset', detail, level='ERROR')

    # Here I am trying to get at the dataset object that is a part of file.
    # I would like to compared its status to that of the file to determine 
    # a mismatch, howeverm this is not working as it does in the upgrade
    # I think that we would need to affect the imbedding but then that gets 
    # circular 

    #context = system['context']
    #root = find_root(context)
    #dataset = root.get_by_uuid(value['dataset'])

    #dataset_status = dataset.get('status')

    #if file_status == 'released' and dataset_status != 'released':
    #    detail = '{} file - {} dataset'.format(file_status, dataset_status)
    #    raise AuditFailure('status mismatch', detail, level='ERROR')

    #if file_status in current_statuses and dataset_status in not_current_statuses:
    #    detail = '{} file - {} dataset'.format(file_status, dataset_status)
    #    raise AuditFailure('status mismatch', detail, level='ERROR')


@audit_checker('file')
def audit_file_output_type(value, system):

    if value.get('status') == 'deleted':
        return

    undesirable_output_type = [
        'Alignability',
        'Base_Overlap_Signal',
        'enhancers_forebrain',
        'enhancers_heart',
        'enhancers_wholebrain',
        'Excludable',
        'ExonsDeNovo',
        'ExonsEnsV65IAcuff',
        'ExonsGencV10',
        'ExonsGencV3c',
        'ExonsGencV7',
        'FiltTransfrags',
        'GeneDeNovo',
        'GeneEnsV65IAcuff',
        'GeneGencV10',
        'GeneGencV3c',
        'GeneGencV7',
        'HMM',
        'Junctions',
        'library_fraction',
        'Matrix',
        'minus signal',
        'mPepMapGcFt',
        'mPepMapGcUnFt'
        'PctSignal'
        'pepMapGcFt',
        'pepMapGcUnFt',
        'Primer',
        'PrimerPeaks',
        'RbpAssocRna',
        'SumSignal',
        'TranscriptDeNovo',
        'TranscriptEnsV65IAcuff',
        'TranscriptGencV10',
        'TranscriptGencV3c',
        'TranscriptGencV7',
        'Transfrags',
        'TssGencV3c',
        'TssGencV7',
        'TssHmm',
        'UniformlyProcessedPeakCalls',
        'Uniqueness',
        'Validation',
        'Valleys',
        'WaveSignal',
        ]

    #if value['dataset']['award']['rfa'] != 'ENCODE3':
    if value['output_type'] in undesirable_output_type:
            detail = '{}'.format(value['output_type'])
            raise AuditFailure('undesirable output type', detail, level='DCC_ACTION')
