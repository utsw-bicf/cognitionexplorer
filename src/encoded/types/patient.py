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
    name="patients",
    unique_key="accession",
    properties={
        "title": "Patients",
        "description": "Redcap master_id forms: Basic patient information pages",
    },
)
class Patient(Item):
    item_type = "patient"
    schema = load_schema("encoded:schemas/patient.json")
    name_key ="accession"
    embedded = [
        'ivp_a1',
        'fvp_a1',
        'ivp_a2',
        'fvp_a2',
        'ivp_a5',
        'ivp_b5',
        'ivp_b6',
        'ivp_b4',
        'ivp_b1',
        'ivp_b7',
        'ivp_b8',
    ]
    rev = {
        'ivp_a1': ('Ivp_a1', 'patient'),
        'fvp_a1': ('Fvp_a1', 'patient'),
        'ivp_a2': ('Ivp_a2', 'patient'),
        'fvp_a2': ('Fvp_a2', 'patient'),
        'ivp_b1': ('Ivp_b1', 'patient'),
        'ivp_a5': ('Ivp_a5', 'patient'),
        'ivp_b5': ('Ivp_b5', 'patient'),
        'ivp_b6': ('Ivp_b6', 'patient'),
        'ivp_b4': ('Ivp_b4', 'patient'),
        'ivp_b7': ('Ivp_b7', 'patient'),
        'ivp_b8': ('Ivp_b8', 'patient'),


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
        "title": "Ivp_b1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b1"
        },
    })
    def ivp_b1(self, request, ivp_b1):
        return paths_filtered_by_status(request, ivp_b1)
    
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

    @calculated_property(schema={
        "title": "Ivp_b4",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b4"
        },
    })
    def ivp_b4(self, request, ivp_b4):
        return paths_filtered_by_status(request, ivp_b4)
    
    @calculated_property(schema={
        "title": "Ivp_b5",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b5"
        },
    })
    def ivp_b5(self, request, ivp_b5):
        return paths_filtered_by_status(request, ivp_b5)
       
    @calculated_property(schema={
        "title": "Ivp_b6",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b6"
        },
    })
    def ivp_b6(self, request, ivp_b6):
        return paths_filtered_by_status(request, ivp_b6)
        
    @calculated_property(schema={
        "title": "Ivp_b7",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b7"
        },
    })
    def ivp_b7(self, request, ivp_b7):
        return paths_filtered_by_status(request, ivp_b7)

    @calculated_property(schema={
        "title": "Ivp_b8",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b8"
        },
    })
    def ivp_b8(self, request, ivp_b8):
        return paths_filtered_by_status(request, ivp_b8)
