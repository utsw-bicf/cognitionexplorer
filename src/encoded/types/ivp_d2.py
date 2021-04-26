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
    name="ivp_d2s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_D2 Forms",
        "description": "UDS Initial visiting patients D2 forms results pages",
    })
class Ivp_d2(Item):
    base_types = ['Ivp_d2'] + Item.base_types
    embedded = [
        
    ]
    rev = {
    }


audit_inherit = []
set_status_up = []
set_status_down = []


@collection(
    name='ivp_d2v3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_D2V3 Forms",
        "description": "UDS Initial visiting patients D2V3 forms results pages",
    })
class Ivp_d2v3(Ivp_d2):
    item_type = 'ivp_d2v3'
    schema = load_schema('encoded:schemas/ivp_d2v3.json')
    embedded = Ivp_d2.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []


@collection(
    name='ivp_d2v2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_D2V2 Forms",
        "description": "UDS Initial visiting patients D2V2 forms results pages",
    })
class Ivp_d2v2(Ivp_d2):
    item_type = 'ivp_d2v2'
    schema = load_schema('encoded:schemas/ivp_d2v2.json')
    embedded = Ivp_d2.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
