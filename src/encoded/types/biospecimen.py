from snovault import (
    calculated_property,
    collection,
    load_schema,
)
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


