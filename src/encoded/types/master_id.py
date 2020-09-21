from snovault import (
    calculated_property,
    collection,
    load_schema,
)
from .base import (
    Item,
    # SharedItem,
    paths_filtered_by_status,
)
from pyramid.traversal import find_root, resource_path

import re

@collection(
    name="master_ids",
    unique_key="accession",
    properties={
        "title": "Redcap_master_id Forms",
        "description": "Redcap master_id forms: Basic patient information pages",
    },
)
class Master_id(Item):
    item_type = "master_id"
    schema = load_schema("encoded:schemas/master_id.json")
    name_key ="accession"
    embedded = [
        'ivp_a1',
        'fvp_a1',
        'ivp_a2',
        'ivp_a5',
        'fvp_a2'

    ]
    rev = {
        'ivp_a1': ('Ivp_a1', 'master_id'),
        'fvp_a1': ('Fvp_a1', 'master_id'),
        'ivp_a2': ('Ivp_a2', 'master_id'),
        'ivp_a5': ('Ivp_a2', 'master_id'),
        'fvp_a2': ('Fvp_a2', 'master_id')



    }

    audit_inherit = [
        
    ]
    set_status_up = []
    set_status_down = []

    @calculated_property(schema={
        "title": "Ivp_a1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a1"
        },
    })
    def ivp_a1(self, request, ivp_a1):
        return paths_filtered_by_status(request, ivp_a1)
    
    
    @calculated_property(schema={
        "title": "Fvp_a1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a1"
        },
    })
    def fvp_a1(self, request, fvp_a1):
        return paths_filtered_by_status(request, fvp_a1)
    
    @calculated_property(schema={
        "title": "Ivp_a2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a2"
        },
    })
    def ivp_a2(self, request, ivp_a2):
        return paths_filtered_by_status(request, ivp_a2)

    @calculated_property(schema={
        "title": "Fvp_a2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a2"
        },
    })
    def fvp_a2(self, request, fvp_a2):
        return paths_filtered_by_status(request, fvp_a2)

    @calculated_property(schema={
        "title": "Ivp_a5",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a5"
        },
    })
    def ivp_a5(self, request, ivp_a5):
        return paths_filtered_by_status(request, ivp_a5)
    