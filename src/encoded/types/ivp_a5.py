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
    name="ivp_a5s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_A5 Forms",
        "description": "UDS Initial visiting patients A5 forms results pages",
    })
class Ivp_a5(Item):
    base_types = ['Ivp_a5'] + Item.base_types
    embedded = [
        
    ]
    rev = {
    }


audit_inherit = []
set_status_up = []
set_status_down = []


@collection(
    name='ivp_a5v3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_A5V3 Forms",
        "description": "UDS Initial visiting patients A5V3 forms results pages",
    })
class Ivp_a5v3(Ivp_a5):
    item_type = 'ivp_a5v3'
    schema = load_schema('encoded:schemas/ivp_a5v3.json')
    embedded = Ivp_a5.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []


@collection(
    name='ivp_a5v2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_A5V2 Forms",
        "description": "UDS Initial visiting patients A5V2 forms results pages",
    })
class Ivp_a5v2(Ivp_a5):
    item_type = 'ivp_a5v2'
    schema = load_schema('encoded:schemas/ivp_a5v2.json')
    embedded = Ivp_a5.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
