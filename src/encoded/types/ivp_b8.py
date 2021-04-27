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
    name="ivp_b8s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_B8 Forms",
        "description": "UDS Initial visiting patients B8 forms results pages",
    })
class Ivp_b8(Item):
    base_types = ['Ivp_b8'] + Item.base_types
    embedded = [
        
    ]
    rev = {
    }


audit_inherit = []
set_status_up = []
set_status_down = []


@collection(
    name='ivp_b8v3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B8V3 Forms",
        "description": "UDS Initial visiting patients B8V3 forms results pages",
    })
class Ivp_b8v3(Ivp_b8):
    item_type = 'ivp_b8v3'
    schema = load_schema('encoded:schemas/ivp_b8v3.json')
    embedded = Ivp_b8.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []


@collection(
    name='ivp_b8v2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B8V2 Forms",
        "description": "UDS Initial visiting patients B8V2 forms results pages",
    })
class Ivp_b8v2(Ivp_b8):
    item_type = 'ivp_b8v2'
    schema = load_schema('encoded:schemas/ivp_b8v2.json')
    embedded = Ivp_b8.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
