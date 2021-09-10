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
    name="ivp_c2s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_C2 Forms",
        "description": "UDS Initial visiting patients C2 forms results pages",
    })
class Ivp_c2(Item):
    base_types = ['Ivp_c2'] + Item.base_types
    embedded = [
        
    ]
    rev = {
    }


audit_inherit = []
set_status_up = []
set_status_down = []


@collection(
    name='ivp_c2v3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_C2V3 Forms",
        "description": "UDS Initial visiting patients C2V3 forms results pages",
    })
class Ivp_c2v3(Ivp_c2):
    item_type = 'ivp_c2v3'
    schema = load_schema('encoded:schemas/ivp_c2v3.json')
    embedded = Ivp_c2.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []


@collection(
    name='ivp_c2v2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_C2V2 Forms",
        "description": "UDS Initial visiting patients C2V2 forms results pages",
    })
class Ivp_c2v2(Ivp_c2):
    item_type = 'ivp_c2v2'
    schema = load_schema('encoded:schemas/ivp_c2v2.json')
    embedded = Ivp_c2.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
