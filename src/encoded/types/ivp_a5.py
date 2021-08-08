from snovault import (
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




@collection(
    name='ivp_a5v3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_A5V3 Forms",
        "description": "UDS Initial visiting patients A5V3 forms results pages",
    })
class Ivp_a5v3(Item):
    item_type = 'ivp_a5v3'
    schema = load_schema('encoded:schemas/ivp_a5v3.json')
    embedded = []
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
class Ivp_a5v2(Item):
    item_type = 'ivp_a5v2'
    schema = load_schema('encoded:schemas/ivp_a5v2.json')
    embedded =  []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []

@collection(
    name='ivp_a5v1',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_A5V1 Forms",
        "description": "UDS Initial visiting patients A5V1 forms results pages",
    })
class Ivp_a5v1(Item):
    item_type = 'ivp_a5v1'
    schema = load_schema('encoded:schemas/ivp_a5v1.json')
    embedded =  []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
