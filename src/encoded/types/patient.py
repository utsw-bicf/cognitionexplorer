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
    name_key = "accession"
    embedded = [
        'ivp_a1v3',
        'ivp_a1v2',
        'ivp_a2v3',
        'ivp_a2v2',
        'ivp_a2v1',
        'ivp_a1v1',
        'fvp_a1v3',
        'fvp_a1v2',
        'tvp_a1',
        'ivp_a3v3',
        'ivp_a3v2',

        'fvp_a2v3',
        'fvp_a2v2',
        'tvp_a2',
        'tvp_a3',
        'ivp_a5v2',
        'fvp_a5v2',

        'ivp_a5v3',
        'ivp_b2v2',
        'ivp_e1v2',
        'fvp_e1v2',
        'fvp_z1v2',
        'ivp_z1v2',
        'fvp_b2v2',
        'fvp_b3v2',
        'ivp_b3v2',

        'ivp_b1v3',
        'ivp_b1v2',

        'fvp_b1v3',
        'fvp_b1v2',
        'ivp_b4v3',
        'ivp_b4v2',
        'ivp_b5v3',
        'ivp_b5v2',
        'fvp_b5v3',
        'fvp_b5v2',
        'tvp_b5',
        'ivp_b6v3',
        'ivp_b6v2',
        'ivp_b7v3',
        'ivp_b7v2',
        'fvp_b7v3',
        'fvp_b7v2',
        'tvp_b7',
        'ivp_b8v3',
        'ivp_b8v2',
        'ivp_b9v2',
        'ivp_b9v3',
        'ivp_c1v2',

        'ivp_c2',
        'fvp_b9v3',
        'fvp_b9v2',
        'fvp_c1v3',
        'fvp_c1v2',
        'ivp_d1v2',
        'ivp_d1v3',
        'fvp_d1v3',
        'fvp_d1v2',
        
        'ivp_d2',
        'ivp_a4v2',
        'ivp_a4v3',
        'fvp_c2v3',
        'fvp_b6v3',
        'fvp_b6v2',
        'fvp_b4v3',
        'fvp_b4v2',
        'fvp_d2v3',
        'm1',
        'fvp_a4v3',
        'fvp_a4v2',
        'tvp_a4',
        'fvp_a3v3',
        'fvp_a3v2',
        'fvp_b8v3',
        'fvp_b8v2',
        'tvp_a1',
        'tvp_z1x',
        'ivp_z1x',
        'fvp_z1xv3',
        'tvp_d2',
        'tvp_t1',
        'tvp_b4',
        'concussion_history',
    ]
    rev = {
        'ivp_a1v3': ('Ivp_a1v3', 'patient'),
        'ivp_a1v2': ('Ivp_a1v2', 'patient'),
        'ivp_a2v3': ('Ivp_a2v3', 'patient'),
        'ivp_a2v2': ('Ivp_a2v2', 'patient'),
        'ivp_a2v1': ('Ivp_a2v1', 'patient'),
        'ivp_a1v1': ('Ivp_a1v1', 'patient'),
        'fvp_a1v3': ('Fvp_a1v3', 'patient'),
        'fvp_a1v2': ('Fvp_a1v2', 'patient'),
        'ivp_a3v3': ('Ivp_a3v3', 'patient'),
        'ivp_a3v2': ('Ivp_a3v2', 'patient'),
        'tvp_a2': ('Tvp_a2', 'patient'),
        'tvp_a3': ('Tvp_a3', 'patient'),
        'fvp_a2v3': ('Fvp_a2v3', 'patient'),
        'fvp_a2v2': ('Fvp_a2v2', 'patient'),
        'ivp_a5v2': ('Ivp_a5v2', 'patient'),
        'fvp_a5v2': ('Fvp_a5v2', 'patient'),
        'ivp_a5v3': ('Ivp_a5v3', 'patient'),
        'ivp_b2v2': ('Ivp_b2v2', 'patient'),
        'ivp_e1v2': ('Ivp_e1v2', 'patient'),
        'fvp_e1v2': ('Fvp_e1v2', 'patient'),
        'fvp_z1v2': ('Fvp_z1v2', 'patient'),
        'fvp_b2v2': ('Fvp_b2v2', 'patient'),
        'fvp_b3v2': ('Fvp_b3v2', 'patient'),
        'ivp_z1v2': ('Ivp_z1v2', 'patient'),
        'ivp_b3v2': ('Ivp_b3v2', 'patient'),

        'ivp_b1v3': ('Ivp_b1v3', 'patient'),
        'ivp_b1v2': ('Ivp_b1v3', 'patient'),

        'fvp_b1v3': ('Fvp_b1v3', 'patient'),
        'fvp_b1v2': ('Fvp_b1v2', 'patient'),
        'ivp_b4v3': ('Ivp_b4v3', 'patient'),
        'ivp_b4v2': ('Ivp_b4v2', 'patient'),
        'ivp_b5v3': ('Ivp_b5v3', 'patient'),
        'ivp_b5v2': ('Ivp_b5v2', 'patient'),
        'fvp_b5v3': ('Fvp_b5v3', 'patient'),
        'fvp_b5v2': ('Fvp_b5v2', 'patient'),
        'tvp_b5': ('Tvp_b5', 'patient'),
        'ivp_b6v3': ('Ivp_b6v3', 'patient'),
        'ivp_b6v2': ('Ivp_b6v2', 'patient'),
        'ivp_b7v3': ('Ivp_b7v3', 'patient'),
        'ivp_b7v2': ('Ivp_b7v2', 'patient'),
        'fvp_b7v3': ('Fvp_b7v3', 'patient'),
        'fvp_b7v2': ('Fvp_b7v2', 'patient'),
        'tvp_b7': ('Tvp_b7', 'patient'),
        'ivp_b8v3': ('Ivp_b8v3', 'patient'),
        'ivp_b8v2': ('Ivp_b8v2', 'patient'),
        'fvp_b8v3': ('Fvp_b8v3', 'patient'),
        'fvp_b8v2': ('Fvp_b8v2', 'patient'),
        'ivp_b9v2': ('Ivp_b9v2', 'patient'),
        'ivp_b9v3': ('Ivp_b9v3', 'patient'),
        'ivp_c2': ('Ivp_c2', 'patient'),
        'ivp_c1v2': ('Ivp_c1v2', 'patient'),
        'fvp_b9v3': ('Fvp_b9v3', 'patient'),
        'fvp_b9v2': ('Fvp_b9v2', 'patient'),
        'fvp_c1v3': ('Fvp_c1v3', 'patient'),
        'fvp_c1v2': ('Fvp_c1v2', 'patient'),
        'ivp_d1v2': ('Ivp_d1v2', 'patient'),
        'ivp_d1v3': ('Ivp_d1v3', 'patient'),
        'fvp_d1v3': ('Fvp_d1v3', 'patient'),
        'fvp_d1v2': ('Fvp_d1v2', 'patient'),
        'ivp_d2': ('Ivp_d2', 'patient'),
        'ivp_a4v2': ('Ivp_a4v2', 'patient'),
        'ivp_a4v3': ('Ivp_a4v3', 'patient'),
        'fvp_c2v3': ('Fvp_c2v3', 'patient'),
        'fvp_b6v3': ('Fvp_b6v3', 'patient'),
        'fvp_b6v2': ('Fvp_b6v2', 'patient'),
        'fvp_b4v3': ('Fvp_b4v3', 'patient'),
        'fvp_b4v2': ('Fvp_b4v2', 'patient'),
        'fvp_d2v3': ('Fvp_d2v3', 'patient'),
        'm1': ('M1', 'patient'),
        'fvp_a4v3': ('Fvp_a4v3', 'patient'),
        'fvp_a4v2': ('Fvp_a4v2', 'patient'),
        'tvp_a4': ('Tvp_a4', 'patient'),
        'fvp_a3v3': ('Fvp_a3v3', 'patient'),
        'fvp_a3v2': ('Fvp_a3v2', 'patient'),
        'tvp_a1': ('Tvp_a1', 'patient'),
        'tvp_z1x': ('Tvp_z1x', 'patient'),
        'ivp_z1x': ('Ivp_z1x', 'patient'),
        'fvp_z1xv3': ('Fvp_z1xv3', 'patient'),
        'tvp_d2': ('Tvp_d2', 'patient'),
        'tvp_t1': ('Tvp_t1', 'patient'),
        'tvp_b4': ('Tvp_b4', 'patient'),
        'concussion_history': ('Concussion_history', 'patient'),
    }

    audit_inherit = [

    ]
    set_status_up = []
    set_status_down = []

    @calculated_property(schema={
        "title": "Ivp_a1v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a1v3"
        },
    })
    def ivp_a1v3(self, request, ivp_a1v3):
        return paths_filtered_by_status(request, ivp_a1v3)

    @calculated_property(schema={
        "title": "Ivp_a1v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a1v2"
        },
    })
    def ivp_a1v2(self, request, ivp_a1v2):
        return paths_filtered_by_status(request, ivp_a1v2)

    @calculated_property(schema={
        "title": "Ivp_a2v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a2v3"
        },
    })
    def ivp_a2v3(self, request, ivp_a2v3):
        return paths_filtered_by_status(request, ivp_a2v3)

    @calculated_property(schema={
        "title": "Ivp_a2v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a2v2"
        },
    })
    def ivp_a2v2(self, request, ivp_a2v2):
        return paths_filtered_by_status(request, ivp_a2v2)

    @calculated_property(schema={
        "title": "Ivp_a2v1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a2v1"
        },
    })
    def ivp_a2v1(self, request, ivp_a2v1):
        return paths_filtered_by_status(request, ivp_a2v1)

    @calculated_property(schema={
        "title": "Ivp_a1v1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a1v1"
        },
    })
    def ivp_a1v1(self, request, ivp_a1v1):
        return paths_filtered_by_status(request, ivp_a1v1)

    @calculated_property(schema={
        "title": "Fvp_a1v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a1v3"
        },
    })
    def fvp_a1v3(self, request, fvp_a1v3):
        return paths_filtered_by_status(request, fvp_a1v3)

    @calculated_property(schema={
        "title": "Fvp_a1v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a1v2"
        },
    })
    def fvp_a1v2(self, request, fvp_a1v2):
        return paths_filtered_by_status(request, fvp_a1v2)

    @calculated_property(schema={
        "title": "Ivp_a3v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a3v3"
        },
    })
    def ivp_a3v3(self, request, ivp_a3v3):
        return paths_filtered_by_status(request, ivp_a3v3)

    @calculated_property(schema={
        "title": "Ivp_a3v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a3v2"
        },
    })
    def ivp_a3v2(self, request, ivp_a3v2):
        return paths_filtered_by_status(request, ivp_a3v2)
    @calculated_property(schema={
        "title": "Fvp_a2v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a2v3"
        },
    })
    def fvp_a2v3(self, request, fvp_a2v3):
        return paths_filtered_by_status(request, fvp_a2v3)

    @calculated_property(schema={
        "title": "Fvp_a2v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a2v2"
        },
    })
    def fvp_a2v2(self, request, fvp_a2v2):
        return paths_filtered_by_status(request, fvp_a2v2)

    @calculated_property(schema={
        "title": "Ivp_b1v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b1v3"
        },
    })
    def ivp_b1v3(self, request, ivp_b1v3):
        return paths_filtered_by_status(request, ivp_b1v3)

    @calculated_property(schema={
        "title": "Ivp_b1v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b1v2"
        },
    })
    def ivp_b1v2(self, request, ivp_b1v2):
        return paths_filtered_by_status(request, ivp_b1v2)

    @calculated_property(schema={
        "title": "Ivp_a5v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a5v2"
        },
    })
    def ivp_a5v2(self, request, ivp_a5v2):
        return paths_filtered_by_status(request, ivp_a5v2)

    @calculated_property(schema={
        "title": "Fvp_a5v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a5v2"
        },
    })
    def fvp_a5v2(self, request, fvp_a5v2):
        return paths_filtered_by_status(request, fvp_a5v2)
        
    @calculated_property(schema={
        "title": "Ivp_a5v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a5v3"
        },
    })
    def ivp_a5v3(self, request, ivp_a5v3):
        return paths_filtered_by_status(request, ivp_a5v3)


    @calculated_property(schema={
        "title": "Ivp_b2v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b2v2"
        },
    })
    def ivp_b2v2(self, request, ivp_b2v2):
        return paths_filtered_by_status(request, ivp_b2v2)

    @calculated_property(schema={
        "title": "Ivp_b3v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b3v2"
        },
    })
    def ivp_b3v2(self, request, ivp_b3v2):
        return paths_filtered_by_status(request, ivp_b3v2)

    @calculated_property(schema={
        "title": "Ivp_b4v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b4v3"
        },
    })
    def ivp_b4v3(self, request, ivp_b4v3):
        return paths_filtered_by_status(request, ivp_b4v3)

    @calculated_property(schema={
        "title": "Ivp_b4v2",
        "type": "array",
        "items": {
                "type": 'string',
                "linkTo": "Ivp_b4v2"
        },
    })
    def ivp_b4v2(self, request, ivp_b4v2):
        return paths_filtered_by_status(request, ivp_b4v2)

    @calculated_property(schema={
        "title": "Ivp_b5v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b5v3"
        },
    })
    def ivp_b5v3(self, request, ivp_b5v3):
        return paths_filtered_by_status(request, ivp_b5v3)

    @calculated_property(schema={
        "title": "Ivp_b5v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b5v2"
        },
    })
    def ivp_b5v2(self, request, ivp_b5v2):
        return paths_filtered_by_status(request, ivp_b5v2)

    @calculated_property(schema={
        "title": "Ivp_b6v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b6v3"
        },
    })
    def ivp_b6v3(self, request, ivp_b6v3):
        return paths_filtered_by_status(request, ivp_b6v3)

    @calculated_property(schema={
        "title": "Ivp_b6v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b6v2"
        },
    })
    def ivp_b6v2(self, request, ivp_b6v2):
        return paths_filtered_by_status(request, ivp_b6v2)

    @calculated_property(schema={
        "title": "Ivp_b7v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b7v3"
        },
    })
    def ivp_b7v3(self, request, ivp_b7v3):
        return paths_filtered_by_status(request, ivp_b7v3)

    @calculated_property(schema={
        "title": "Ivp_b7v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b7v2"
        },
    })
    def ivp_b7v2(self, request, ivp_b7v2):
        return paths_filtered_by_status(request, ivp_b7v2)

    @calculated_property(schema={
        "title": "Ivp_b8v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b8v3"
        },
    })
    def ivp_b8v3(self, request, ivp_b8v3):
        return paths_filtered_by_status(request, ivp_b8v3)

    @calculated_property(schema={
        "title": "Ivp_b8v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b8v2"
        },
    })
    def ivp_b8v2(self, request, ivp_b8v2):
        return paths_filtered_by_status(request, ivp_b8v2)
    
    @calculated_property(schema={
        "title": "Ivp_b9v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b9v2"
        },
    })
    def ivp_b9v2(self, request, ivp_b9v2):
        return paths_filtered_by_status(request, ivp_b9v2)
    
    @calculated_property(schema={
        "title": "Ivp_b9v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b9v3"
        },
    })
    def ivp_b9v3(self, request, ivp_b9v3):
        return paths_filtered_by_status(request, ivp_b9v3)
    

    @calculated_property(schema={
        "title": "Ivp_c2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_c2"
        },
    })
    def ivp_c2(self, request, ivp_c2):
        return paths_filtered_by_status(request, ivp_c2)

    @calculated_property(schema={
        "title": "Ivp_c1v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_c1v2"
        },
    })
    def ivp_c1v2(self, request, ivp_c1v2):
        return paths_filtered_by_status(request, ivp_c1v2)

    @calculated_property(schema={
        "title": "Ivp_d1v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_d1v2"
        },
    })
    def ivp_d1v2(self, request, ivp_d1v2):
        return paths_filtered_by_status(request, ivp_d1v2)

    @calculated_property(schema={
        "title": "Ivp_d1v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_d1v3"
        },
    })
    def ivp_d1v3(self, request, ivp_d1v3):
        return paths_filtered_by_status(request, ivp_d1v3)

    @calculated_property(schema={
        "title": "Ivp_d2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_d2"
        },
    })
    def ivp_d2(self, request, ivp_d2):
        return paths_filtered_by_status(request, ivp_d2)

    @calculated_property(schema={
        "title": "Ivp_e1v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_e1v2"
        },
    })
    def ivp_e1v2(self, request, ivp_e1v2):
        return paths_filtered_by_status(request, ivp_e1v2)

    @calculated_property(schema={
        "title": "Fvp_e1v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_e1v2"
        },
    })
    def fvp_e1v2(self, request, fvp_e1v2):
        return paths_filtered_by_status(request, fvp_e1v2)

    @calculated_property(schema={
        "title": "Fvp_z1v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_z1v2"
        },
    })
    def fvp_z1v2(self, request, fvp_z1v2):
        return paths_filtered_by_status(request, fvp_z1v2)

    @calculated_property(schema={
        "title": "Fvp_b2v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b2v2"
        },
    })
    def fvp_b2v2(self, request, fvp_b2v2):
        return paths_filtered_by_status(request, fvp_b2v2)

    @calculated_property(schema={
        "title": "Fvp_b3v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b3v2"
        },
    })
    def fvp_b3v2(self, request, fvp_b3v2):
        return paths_filtered_by_status(request, fvp_b3v2)

    @calculated_property(schema={
        "title": "Ivp_z1v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_z1v2"
        },
    })
    def ivp_z1v2(self, request, ivp_z1v2):
        return paths_filtered_by_status(request, ivp_z1v2)

    @calculated_property(schema={
        "title": "Ivp_a4v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a4v3"
        },
    })
    def ivp_a4v3(self, request, ivp_a4v3):
        return paths_filtered_by_status(request, ivp_a4v3)

    @calculated_property(schema={
        "title": "Ivp_a4v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a4v2"
        },
    })
    def ivp_a4v2(self, request, ivp_a4v2):
        return paths_filtered_by_status(request, ivp_a4v2)

    @calculated_property(schema={
        "title": "Fvp_c2v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_c2v3"
        },
    })
    def fvp_c2v3(self, request, fvp_c2v3):
        return paths_filtered_by_status(request, fvp_c2v3)

    @calculated_property(schema={
        "title": "Fvp_b6v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b6v3"
        },
    })
    def fvp_b6v3(self, request, fvp_b6v3):
        return paths_filtered_by_status(request, fvp_b6v3)

    @calculated_property(schema={
        "title": "Fvp_b6v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b6v2"
        },
    })
    def fvp_b6v2(self, request, fvp_b6v2):
        return paths_filtered_by_status(request, fvp_b6v2)

    @calculated_property(schema={
        "title": "Fvp_b4v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b4v3"
        },
    })
    def fvp_b4v3(self, request, fvp_b4v3):
        return paths_filtered_by_status(request, fvp_b4v3)

    @calculated_property(schema={
        "title": "Fvp_b4v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b4v2"
        },
    })
    def fvp_b4v2(self, request, fvp_b4v2):
        return paths_filtered_by_status(request, fvp_b4v2)

    @calculated_property(schema={
        "title": "Fvp_c1v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_c1v3"
        },
    })
    def fvp_c1v3(self, request, fvp_c1v3):
        return paths_filtered_by_status(request, fvp_c1v3)

    @calculated_property(schema={
        "title": "Fvp_c1v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_c1v2"
        },
    })
    def fvp_c1v2(self, request, fvp_c1v2):
        return paths_filtered_by_status(request, fvp_c1v2)

    @calculated_property(schema={
        "title": "Fvp_a3v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a3v3"
        },
    })
    def fvp_a3v3(self, request, fvp_a3v3):
        return paths_filtered_by_status(request, fvp_a3v3)

    @calculated_property(schema={
        "title": "Fvp_a3v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a3v2"
        },
    })
    def fvp_a3v2(self, request, fvp_a3v2):
        return paths_filtered_by_status(request, fvp_a3v2)
        
    @calculated_property(schema={
        "title": "Fvp_b9v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b9v3"
        },
    })
    def fvp_b9v3(self, request, fvp_b9v3):
        return paths_filtered_by_status(request, fvp_b9v3)

    @calculated_property(schema={
        "title": "Fvp_b9v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b9v2"
        },
    })
    def fvp_b9v2(self, request, fvp_b9v2):
        return paths_filtered_by_status(request, fvp_b9v2)

    @calculated_property(schema={
        "title": "Fvp_b7v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b7v3"
        },
    })
    def fvp_b7v3(self, request, fvp_b7v3):
        return paths_filtered_by_status(request, fvp_b7v3)
    
    @calculated_property(schema={
        "title": "Fvp_b7v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b7v2"
        },
    })
    def fvp_b7v2(self, request, fvp_b7v2):
        return paths_filtered_by_status(request, fvp_b7v2)

    @calculated_property(schema={
        "title": "Fvp_b5v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b5v3"
        },
    })
    def fvp_b5v3(self, request, fvp_b5v3):
        return paths_filtered_by_status(request, fvp_b5v3)

    @calculated_property(schema={
        "title": "Fvp_b5v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b5v2"
        },
    })
    def fvp_b5v2(self, request, fvp_b5v2):
        return paths_filtered_by_status(request, fvp_b5v2)

    @calculated_property(schema={
        "title": "Fvp_b1v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b1v3"
        },
    })
    def fvp_b1v3(self, request, fvp_b1v3):
        return paths_filtered_by_status(request, fvp_b1v3)

    @calculated_property(schema={
        "title": "Fvp_b1v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b1v2"
        },
    })
    def fvp_b1v2(self, request, fvp_b1v2):
        return paths_filtered_by_status(request, fvp_b1v2)

    @calculated_property(schema={
        "title": "Fvp_d2v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_d2v3"
        },
    })
    def fvp_d2v3(self, request, fvp_d2v3):
        return paths_filtered_by_status(request, fvp_d2v3)

    @calculated_property(schema={
        "title": "Fvp_b8v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b8v3"
        },
    })
    def fvp_b8v3(self, request, fvp_b8v3):
        return paths_filtered_by_status(request, fvp_b8v3)

    @calculated_property(schema={
        "title": "Fvp_b8v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b8v2"
        },
    })
    def fvp_b8v2(self, request, fvp_b8v2):
        return paths_filtered_by_status(request, fvp_b8v2)

    @calculated_property(schema={
        "title": "Fvp_d1v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_d1v3"
        },
    })
    def fvp_d1v3(self, request, fvp_d1v3):
        return paths_filtered_by_status(request, fvp_d1v3)

    @calculated_property(schema={
        "title": "Fvp_d1v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_d1v2"
        },
    })
    def fvp_d1v2(self, request, fvp_d1v2):
        return paths_filtered_by_status(request, fvp_d1v2)

    @calculated_property(schema={
        "title": "Tvp_a1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Tvp_a1"
        },
    })
    def tvp_a1(self, request, tvp_a1):
        return paths_filtered_by_status(request, tvp_a1)

    @calculated_property(schema={
        "title": "Tvp_a3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Tvp_a3"
        },
    })
    def tvp_a3(self, request, tvp_a3):
        return paths_filtered_by_status(request, tvp_a3)

    @calculated_property(schema={
        "title": "Tvp_z1x",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Tvp_z1x"
        },
    })
    def tvp_z1x(self, request, tvp_z1x):
        return paths_filtered_by_status(request, tvp_z1x)

    @calculated_property(schema={
        "title": "Ivp_z1x",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_z1x"
        },
    })
    def ivp_z1x(self, request, ivp_z1x):
        return paths_filtered_by_status(request, ivp_z1x)

    @calculated_property(schema={
        "title": "Fvp_z1xv3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_z1xv3"
        },
    })
    def fvp_z1xv3(self, request, fvp_z1xv3):
        return paths_filtered_by_status(request, fvp_z1xv3)

    @calculated_property(schema={
        "title": "Tvp_d2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Tvp_d2"
        },
    })
    def tvp_d2(self, request, tvp_d2):
        return paths_filtered_by_status(request, tvp_d2)

    @calculated_property(schema={
        "title": "Tvp_t1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Tvp_t1"
        },
    })
    def tvp_t1(self, request, tvp_t1):
        return paths_filtered_by_status(request, tvp_t1)

    @calculated_property(schema={
        "title": "Tvp_b4",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Tvp_b4"
        },
    })
    def tvp_b4(self, request, tvp_b4):
        return paths_filtered_by_status(request, tvp_b4)

    @calculated_property(schema={
        "title": "Tvp_b7",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Tvp_b7"
        },
    })
    def tvp_b7(self, request, tvp_b7):
        return paths_filtered_by_status(request, tvp_b7)

    @calculated_property(schema={
        "title": "Tvp_b5",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Tvp_b5"
        },
    })
    def tvp_b5(self, request, tvp_b5):
        return paths_filtered_by_status(request, tvp_b5)

    @calculated_property(schema={
        "title": "Tvp_a2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Tvp_a2"
        },
    })
    def tvp_a2(self, request, tvp_a2):
        return paths_filtered_by_status(request, tvp_a2)

    @calculated_property(schema={
        "title": "M1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "M1"
        },
    })
    def m1(self, request, m1):
        return paths_filtered_by_status(request, m1)

    @calculated_property(schema={
        "title": "Fvp_a4v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a4v3"
        },
    })
    def fvp_a4v3(self, request, fvp_a4v3):
        return paths_filtered_by_status(request, fvp_a4v3)

    @calculated_property(schema={
        "title": "Fvp_a4v2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a4v2"
        },
    })
    def fvp_a4v2(self, request, fvp_a4v2):
        return paths_filtered_by_status(request, fvp_a4v2)

    @calculated_property(schema={
        "title": "Tvp_a4",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Tvp_a4"
        },
    })
    def tvp_a4(self, request, tvp_a4):
        return paths_filtered_by_status(request, tvp_a4)

    @calculated_property(schema={
        "title": "Concussion_history",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Concussion_history"
        },
    })
    def concussion_history(self, request, concussion_history):
        return paths_filtered_by_status(request, concussion_history)
