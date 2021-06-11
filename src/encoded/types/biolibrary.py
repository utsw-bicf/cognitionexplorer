from snovault import (
    calculated_property,
    collection,
    load_schema,
)
from pyramid.security import (
    Allow,
    Deny,
    Everyone,
)
from .base import (
    Item,
    paths_filtered_by_status,
)
import re


@collection(
    name='biolibraries',
    unique_key='accession',
    properties={
        'title': 'Biolibraries',
        'description': 'Biolibraries used or available',
    })
class Biolibrary(Item):
    item_type = 'biolibrary'
    schema = load_schema('encoded:schemas/biolibrary.json')
    name_key = 'accession'
    rev = {
        'biofile': ('biofile', 'biolibrary'),
        'bioreplicate': ('bioreplicate', 'biolibrary'),
    }
    embedded = [
        'biospecimen',
        'biospecimen.documents',
        'biofile',
        'bioreplicate',
        'documents'
    ]
    audit_inherit = [
    ]
    set_status_up = [

    ]
    set_status_down = []
    STATUS_ACL = {
        'released': [(Allow, 'group.verification', ['view_details'])]
    }
    
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
        "title": "bioreplicate",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "bioreplicate"
        },
    })
    def bioreplicate(self, request, bioreplicate):
        return paths_filtered_by_status(request, bioreplicate)
