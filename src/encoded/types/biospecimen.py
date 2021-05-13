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
        # 'patient',
        # 'patient.consent',
        'surgery',
        'surgery.surgery_procedure.pathology_report',
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
                "item_status": {
                    "title": "Item Status",
                    "type": "string",
                }
            }
        })
    def genomic_release(self, request, patient):

        consent_list = request.embed(patient, '@@object?skip_calculated=true').get('consent')
        print('consent_list', consent_list)
        consent_type_list=[]
        genomic_release='N'
        item_status='revoked'
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
                # print('consent filter',consent_filter)




            consent_type_list.sort(key= lambda consent_filter:consent_filter['version'])

            consent_lastest=consent_type_list[-1]
            consent_version=consent_lastest['version']
            print ("consent_version",consent_version)

            if consent_version=='1' :
                genomic_release='N'
                item_status='revoked'
            elif consent_version=='2':
                if consent_lastest.get('genetic') is not None:
                    genomic_release = consent_lastest.get('genetic')
                if genomic_release == 'Y':
                    item_status='released'
                    # print('consent 2', genomic_release, item_status)
                else:
                    item_status='revoked'
                    # print('consent 2-N', genomic_release, item_status)
            elif consent_version=='3':
                genomic_release='N'
                item_status='revoked'
            elif consent_version=='4':
                genomic_release='Y'
                item_status='released'
            elif consent_version=='5' or consent_version=='6':
                genomic_release='Y'
                item_status='released'
            else:
                genomic_release='N'
                item_status='revoked'

        genomic_consent = dict()
        genomic_consent['genomic_release'] = genomic_release
        genomic_consent['item_status'] = item_status
        return genomic_consent

    @calculated_property( schema={
        "title": "Anatomic Site",
        "type": "string",
    })
    def anatomic_site_display(self, request, anatomic_site=None):
        if anatomic_site is not None:
            anatomic_site = anatomic_site.replace(", NOS", "")
        return anatomic_site

    matrix = {
        'y': {
            'facets': [
                'status',
                'sample_type',
                'tissue_derivatives',
                'tissue_type',
                'anatomic_site_display',
                'species',
                'specimen_lineage',
                'activity_status',
                'sur_path_tumor_size',
                'surgery.surgery_procedure.procedure_type',
                'surgery.surgery_procedure.pathology_report.t_stage',
                'surgery.surgery_procedure.pathology_report.n_stage',
                'surgery.surgery_procedure.pathology_report.m_stage',
                'surgery.surgery_procedure.pathology_report.ajcc_tnm_stage',
            ],
            'group_by': ['tissue_type', 'tissue_derivatives'],
            'label': 'collection',
        },
        'x': {
            'facets': [
                'surgery.surgery_procedure.pathology_report.histology_filter',
            ],
            'group_by': 'surgery.surgery_procedure.pathology_report.histology_filter',
            'label': 'histology',
        },
    }
