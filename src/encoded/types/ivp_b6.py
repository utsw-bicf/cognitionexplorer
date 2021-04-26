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
    name="ivp_b6s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_B6 Forms",
        "description": "UDS Initial visiting patients B6 forms results pages",
    })
class Ivp_b6(Item):
    base_types = ['Ivp_b6'] + Item.base_types
    embedded = [
        
    ]
    rev = {
    }


audit_inherit = []
set_status_up = []
set_status_down = []


@collection(
    name='ivp_b6v3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B6V3 Forms",
        "description": "UDS Initial visiting patients B6V3 forms results pages",
    })
class Ivp_b6v3(Ivp_b6):
    item_type = 'ivp_b6v3'
    schema = load_schema('encoded:schemas/ivp_b6v3.json')
    embedded = Ivp_b6.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []


@collection(
    name='ivp_b6v2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B6V2 Forms",
        "description": "UDS Initial visiting patients B6V2 forms results pages",
    })
class Ivp_b6v2(Ivp_b6):
    item_type = 'ivp_b6v2'
    schema = load_schema('encoded:schemas/ivp_b6v2.json')
    embedded = Ivp_b6.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
