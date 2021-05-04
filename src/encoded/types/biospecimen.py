from snovault import (
    calculated_property,
    collection,
    load_schema,
)
# from collections import defaultdict
from .base import (
    Item,
    paths_filtered_by_status,
)
import re

# test changes in biospecimen page to see if patient can be embeded through '@@object?skip_calculated=true'
def genomic_release(request, patient):
        # values_by_key = defaultdict(list)
        # consent=[]
        # consent_type_list=[]
        for path in patient:
            properties = request.embed(path, '@@object?skip_calculated=true')
            sex=properties.get('sex')
            # values_by_key[properties.get('patient')].append(properties)
            # consent = properties.get('consent')
            # return dict(values_by_key)
            return sex
        # 
        
        # if len(consent) > 0:
        #     for path in consent:
        #         properties = request.embed(path, '@@object?skip_calculated=true')
        #         consent_type = properties.get('concent_type')


            # for consent_record in consent:
            #     consent_object = request.embed(consent_record, '@@object')
            #     properties = request.embed(path, '@@object?skip_calculated=true')
            #     consent_type= consent_object['consent_type']
            #     consent_type_list.append(consent_type)
            # consent_type_list.sort()
            # print("consent_type",consent_type_list)

            # consent_version=consent_type_list[-1]
            # print ("consent_version",consent_version)
            # if consent_version=='4' or consent_version=='5' or consent_version=='6':
            #     genomic_release='Yes'
            # else:
            #     genomic_release = "No"
            # return genomic_release

@collection(
    name='biospecimens',
    unique_key='accession',
    properties={
        'title': 'Biospecimens',
        'description': 'Biospecimens used or available',
    })
class Biospecimen(Item):
    item_type = 'biospecimen'
    schema = load_schema('encoded:schemas/biospecimen.json')
    name_key = 'accession'
    rev = {
        'ihc':('Ihc','biospecimen'),
        'biofile': ('Biofile', 'biospecimen'),
    }
    embedded = [
        'biofile',
        'biofile.award',
        'patient',
        'patient.consent',
        'surgery',
        'surgery.pathology_report',
        'surgery.surgery_procedure',
        'ihc',
        'award',
        'documents'
    ]
    audit_inherit = [
    ]
    set_status_up = [
        'originated_from',
    ]
    set_status_down = []

    @calculated_property(schema={
        "title": "Biofile",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Biofile"
        },
    })
    def biofile(self, request, biofile):
        return paths_filtered_by_status(request, biofile)

    @calculated_property(schema={
        "title": "Biospecimen IHC",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ihc"
        },
    })
    def ihc(self, request, ihc):
        return paths_filtered_by_status(request, ihc)

    @calculated_property(define=True, schema={
            "title": "Genomic release",
            # "type": "array",
            "type": "string",
        #     "items": {
        #     "type": "string",
        #     "linkTo": "Patient",
        # },
        })
    def genomic_release(self, request, patient):
        
        return genomic_release(request,patient)
    

    matrix = {
        'y': {
            'facets': [
                'status',
                'sample_type',
                'tissue_derivatives',
                'tissue_type',
                'anatomic_site',
                'species',
                'specimen_lineage',
                'activity_status',
                'sur_path_tumor_size',
                'surgery.surgery_procedure.procedure_type',
                'surgery.pathology_report.t_stage',
                'surgery.pathology_report.n_stage',
                'surgery.pathology_report.m_stage',
                'surgery.pathology_report.ajcc_tnm_stage',
            ],
            'group_by': ['tissue_type', 'tissue_derivatives'],
            'label': 'collection',
        },
        'x': {
            'facets': [
                'surgery.pathology_report.histology_filter',
            ],
            'group_by': 'surgery.pathology_report.histology_filter',
            'label': 'histology',
        },
    }


