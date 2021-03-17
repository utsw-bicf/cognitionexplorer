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
        'tvp_a1',
        'ivp_a2',
        'ivp_a3',
        'fvp_a2',
        'tvp_a2',
        'tvp_a3',
        'ivp_a5',
        'ivp_b1',
        'fvp_b1',
        'ivp_b4',
        'ivp_b5',
        'fvp_b5',
        'tvp_b5',
        'ivp_b6',
        'ivp_b7',
        'fvp_b7',
        'tvp_b7',
        'ivp_b8',
        'ivp_b9',
        'ivp_c2',
        'fvp_b9',
        'fvp_c1',
        'ivp_d1',
        'fvp_d1',
        'ivp_d2',
        'ivp_a4',
        'fvp_c2',
        'fvp_b6',
        'fvp_b4',
        'fvp_d2',
        'm1',
        'fvp_a4',
        'tvp_a4',
        'fvp_a3',
        'fvp_b8',
        'tvp_a1',
        'tvp_z1x',
        'ivp_z1x',
        'fvp_z1x',
        'tvp_d2',
        'tvp_t1',
        'tvp_b4', 
        'updrs', 
    ]
    rev = {
        'ivp_a1': ('Ivp_a1', 'patient'),
        'fvp_a1': ('Fvp_a1', 'patient'),
        'ivp_a2': ('Ivp_a2', 'patient'),
        'ivp_a3': ('Ivp_a3', 'patient'),
        'tvp_a2': ('Tvp_a2', 'patient'),
        'tvp_a3': ('Tvp_a3', 'patient'),
        'fvp_a2': ('Fvp_a2', 'patient'),
        'ivp_a5': ('Ivp_a5', 'patient'),
        'ivp_b1': ('Ivp_b1', 'patient'),
        'fvp_b1': ('Fvp_b1', 'patient'),
        'ivp_b4': ('Ivp_b4', 'patient'),
        'ivp_b5': ('Ivp_b5', 'patient'),
        'fvp_b5': ('Fvp_b5', 'patient'),
        'tvp_b5': ('Tvp_b5', 'patient'),
        'ivp_b6': ('Ivp_b6', 'patient'),
        'ivp_b7': ('Ivp_b7', 'patient'),
        'fvp_b7': ('Fvp_b7', 'patient'),
        'tvp_b7': ('Tvp_b7', 'patient'),
        'ivp_b8': ('Ivp_b8', 'patient'),
        'fvp_b8': ('Fvp_b8', 'patient'),
        'ivp_b9': ('Ivp_b9', 'patient'),
        'ivp_c2': ('Ivp_c2', 'patient'),
        'fvp_b9': ('Fvp_b9', 'patient'),
        'fvp_c1': ('Fvp_c1', 'patient'),
        'ivp_d1': ('Ivp_d1', 'patient'),
        'fvp_d1': ('Fvp_d1', 'patient'),
        'ivp_d2': ('Ivp_d2', 'patient'),
        'ivp_a4': ('Ivp_a4', 'patient'),
        'fvp_c2': ('Fvp_c2', 'patient'),
        'fvp_b6': ('Fvp_b6', 'patient'),
        'fvp_b4': ('Fvp_b4', 'patient'),
        'fvp_d2': ('Fvp_d2', 'patient'),
        'm1': ('M1', 'patient'),
        'fvp_a4': ('Fvp_a4', 'patient'),
        'tvp_a4': ('Tvp_a4', 'patient'),
        'fvp_a3': ('Fvp_a3', 'patient'),
        'tvp_a1': ('Tvp_a1', 'patient'),
        'tvp_z1x': ('Tvp_z1x', 'patient'),
        'ivp_z1x': ('Ivp_z1x', 'patient'),
        'fvp_z1x': ('Fvp_z1x', 'patient'),
        'tvp_d2': ('Tvp_d2', 'patient'),
        'tvp_t1': ('Tvp_t1', 'patient'),
        'tvp_b4': ('Tvp_b4', 'patient'),
        'updrs': ('Updrs', 'patient'),

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
        "title": "Ivp_a3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a3"
        },
    })
    def ivp_a3(self, request, ivp_a3):
        return paths_filtered_by_status(request, ivp_a3)

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

    @calculated_property(schema={
        "title": "Ivp_b9",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_b9"
        },
    })
    def ivp_b9(self, request, ivp_b9):
        return paths_filtered_by_status(request, ivp_b9)

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
        "title": "Ivp_d1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_d1"
        },
    })
    def ivp_d1(self, request, ivp_d1):
        return paths_filtered_by_status(request, ivp_d1)
      
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
        "title": "Ivp_a4",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a4"
        },
    })
    def ivp_a4(self, request, ivp_a4):
        return paths_filtered_by_status(request, ivp_a4)

    @calculated_property(schema={
        "title": "Fvp_c2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_c2"
        },
    })
    def fvp_c2(self, request, fvp_c2):
        return paths_filtered_by_status(request, fvp_c2)

    @calculated_property(schema={
        "title": "Fvp_b6",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b6"
        },
    })
    def fvp_b6(self, request, fvp_b6):
        return paths_filtered_by_status(request, fvp_b6)
      
    @calculated_property(schema={
        "title": "Fvp_b4",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b4"
        },
    })
    def fvp_b4(self, request, fvp_b4):
        return paths_filtered_by_status(request, fvp_b4)
    
    @calculated_property(schema={
        "title": "Fvp_c1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_c1"
        },
    })
    def fvp_c1(self, request, fvp_c1):
        return paths_filtered_by_status(request, fvp_c1)
        
    @calculated_property(schema={
        "title": "Fvp_a3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a3"
        },
    })
    def fvp_a3(self, request, fvp_a3):
        return paths_filtered_by_status(request, fvp_a3)

    @calculated_property(schema={
        "title": "Fvp_b9",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b9"
        },
    })
    def fvp_b9(self, request, fvp_b9):
        return paths_filtered_by_status(request, fvp_b9)
      
    @calculated_property(schema={
        "title": "Fvp_b7",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b7"
        },
    })
    def fvp_b7(self, request, fvp_b7):
        return paths_filtered_by_status(request, fvp_b7)
      
    @calculated_property(schema={
        "title": "Fvp_b5",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b5"
        },
    })
    def fvp_b5(self, request, fvp_b5):
        return paths_filtered_by_status(request, fvp_b5)
      
    @calculated_property(schema={
        "title": "Fvp_b1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b1"
        },
    })
    def fvp_b1(self, request, fvp_b1):
        return paths_filtered_by_status(request, fvp_b1)

    @calculated_property(schema={   
        "title": "Fvp_d2",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_d2"
        },
    })
    def fvp_d2(self, request, fvp_d2):
        return paths_filtered_by_status(request, fvp_d2)
      
    @calculated_property(schema={
        "title": "Fvp_b8",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_b8"
        },
    })
    def fvp_b8(self, request, fvp_b8):
        return paths_filtered_by_status(request, fvp_b8)

    @calculated_property(schema={
        "title": "Fvp_d1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_d1"
        },
    })
    def fvp_d1(self, request, fvp_d1):
        return paths_filtered_by_status(request, fvp_d1)
      

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
        "title": "Fvp_z1x",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_z1x"
        },
    })
    def fvp_z1x(self, request, fvp_z1x):
        return paths_filtered_by_status(request, fvp_z1x)

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
        "title": "Fvp_a4",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a4"
        },
    })
    def fvp_a4(self, request, fvp_a4):
        return paths_filtered_by_status(request, fvp_a4)

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
        "title": "Updrs",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Updrs"
        },
    })
    def updrs(self, request, updrs):
        return paths_filtered_by_status(request, updrs)
