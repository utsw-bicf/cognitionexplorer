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
    name="ivp_b7s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_B7 Forms",
        "description": "UDS Initial visiting patients B7 forms results pages",
    })
class Ivp_b7(Item):
    base_types = ['Ivp_b7'] + Item.base_types
    embedded = [
        
    ]
    rev = {
    }


audit_inherit = []
set_status_up = []
set_status_down = []


@collection(
    name='ivp_b7v3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B7V3 Forms",
        "description": "UDS Initial visiting patients B7V3 forms results pages",
    })
class Ivp_b7v3(Ivp_b7):
    item_type = 'ivp_b7v3'
    schema = load_schema('encoded:schemas/ivp_b7v3.json')
    embedded = Ivp_b7.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []


@collection(
    name='ivp_b7v2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B7V2 Forms",
        "description": "UDS Initial visiting patients B7V2 forms results pages",
    })
class Ivp_b7v2(Ivp_b7):
    item_type = 'ivp_b7v2'
    schema = load_schema('encoded:schemas/ivp_b7v2.json')
    embedded = Ivp_b7.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
