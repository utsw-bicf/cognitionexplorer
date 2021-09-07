from pyramid.view import (
    view_config,
)
from pyramid.security import (
    Allow,
    Deny,
    Everyone,
)
from pyramid.traversal import find_root
from snovault import (
    calculated_property,
    collection,
    load_schema,
)
from .base import (
    Item,
    SharedItem,
    paths_filtered_by_status,
)
# from .histology_filters import histology_filters
from snovault.resource_views import item_view_object
from snovault.util import expand_path
from collections import defaultdict
from datetime import datetime
import math






@collection(
     name='patients',
     unique_key='accession',
     properties={
         'title': 'Patients',
         'description': 'Listing Patients',
     })
class Patient(Item):
    item_type = 'patient'
    schema = load_schema('encoded:schemas/patient.json')
    name_key = 'accession'
    embedded = [
        'ivp_a1v3',
        
        ]
    rev = {
         'ivp_a1v3': ('Ivp_a1v3', 'patient'),
       
    }
    set_status_up = [
      


    ]
    set_status_down = []
    STATUS_ACL = {
    }


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
