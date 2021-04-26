from snovault import (
    abstract_collection,
    calculated_property,
    collection,
    load_schema,
)
# from snovault.util import Path
from pyramid.security import Authenticated
from .base import (
    Item,
    paths_filtered_by_status,
)
import re


@abstract_collection(
    name="ivp_b5s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_B5 Forms",
        "description": "UDS Initial visiting patients B5 forms results pages",
    })
class Ivp_b5(Item):
    base_types = ['Ivp_b5'] + Item.base_types
    embedded = [
        
    ]
    rev = {
    }


audit_inherit = []
set_status_up = []
set_status_down = []


@collection(
    name='ivp_b5v3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B5V3 Forms",
        "description": "UDS Initial visiting patients B5V3 forms results pages",
    })
class Ivp_b5v3(Ivp_b5):
    item_type = 'ivp_b5v3'
    schema = load_schema('encoded:schemas/ivp_b5v3.json')
    embedded = Ivp_b5.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []


@collection(
    name='ivp_b5v2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B5V2 Forms",
        "description": "UDS Initial visiting patients B5V2 forms results pages",
    })
class Ivp_b5v2(Ivp_b5):
    item_type = 'ivp_b5v2'
    schema = load_schema('encoded:schemas/ivp_b5v2.json')
    embedded = Ivp_b5.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
