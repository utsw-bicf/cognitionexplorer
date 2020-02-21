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
        'biolibrary': ('Biolibrary', 'biospecimen'),
        'ihc':('Ihc','biospecimen')
    }
    embedded = [
        'biolibrary',
        'biolibrary.biofile',
        'ihc'
    ]
    audit_inherit = [
    ]
    set_status_up = [
        'originated_from',
    ]
    set_status_down = []

    @calculated_property(schema={
        "title": "Biolibrary",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Biolibrary"
        },
    })
    def biolibrary(self, request, biolibrary):
        return paths_filtered_by_status(request, biolibrary)

    @calculated_property(schema={
        "title": "Biospecimen Ihc",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ihc"
        },
    })
    def ihc(self, request, ihc):
        return paths_filtered_by_status(request, ihc)

# @collection(
#     name="Biospecimen ihc",
#     properties={"title": "Biospecimen ihc linked", "description": "Biospecimen ihc results pages",},
# )
# class Ihc(Item):
#     item_type = "ihc"
#     schema = load_schema("encoded:schemas/ihc.json")
#     embeded = []


