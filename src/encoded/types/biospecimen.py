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

    @calculated_property(condition='patient', schema={
            "title": "Genomic release",
            "type": "object",
            "additionalProperties": False,
            "properties":{
                "genomic_release": {
                    "title": "Genomic Release",
                    "type": "string",
                },
                "biospecimen_status": {
                    "title": "Biospecimen Status",
                    "type": "string",
                }
            }
        })
    def genomic_release(self, request, patient):
        consent_list = request.embed(patient, '@@object?skip_calculated=true').get('consent')
        consent_type_list=[]
        genomic_release='N'
        biospecimen_status='revoked'
        if consent_list:
            for consent in consent_list:
                properties = request.embed(consent, '@@object?skip_calculated=true')
                consent_object = request.embed(properties, '@@object')
                version= consent_object['consent_type']
                date=consent_object['date_signed']
                genetic=consent_object['genetic_release']
                consent_filter={}
                consent_filter={'date':date,'version':version,'genetic':genetic}
                # print('consent filter',consent_filter)
                consent_type_list.append(consent_filter)
            consent_type_list.sort(key= lambda consent_filter:consent_filter['version'])

            consent_lastest=consent_type_list[-1]
            consent_version=consent_lastest['version']
            if consent_version=='1' :
                genomic_release='N'
                biospecimen_status='revoked'
            elif consent_version=='2':
                if consent_lastest.get('genetic') is not None:
                    genomic_release = consent_lastest.get('genetic')
                if genomic_release == 'Y':
                    biospecimen_status='revoked'
                    print('consent 2', genomic_release, biospecimen_status)
                else:
                    biospecimen_status='released'
                    print('consent 2-N', genomic_release, biospecimen_status)
            elif consent_version=='3':
                genomic_release='N'
                biospecimen_status='revoked'
            elif consent_version=='4':
                genomic_release='Y'
                biospecimen_status='released'
            elif consent_version=='5' or consent_version=='6':
                genomic_release='Y'
                biospecimen_status='released'
            else:
                genomic_release='N'
                biospecimen_status='revoked'

        genomic_consent = dict()
        genomic_consent['genomic_release'] = genomic_release
        genomic_consent['biospecimen_status'] = biospecimen_status
        return genomic_consent



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
