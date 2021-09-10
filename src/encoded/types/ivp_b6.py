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
    name='ivp_b6v3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B6V3 Forms",
        "description": "UDS Initial visiting patients B6V3 forms results pages",
    })
class Ivp_b6v3(Item):
    item_type = 'ivp_b6v3'
    schema = load_schema('encoded:schemas/ivp_b6v3.json')
    embedded = []
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
class Ivp_b6v2(Item):
    item_type = 'ivp_b6v2'
    schema = load_schema('encoded:schemas/ivp_b6v2.json')
    embedded = []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []

@collection(
    name='ivp_b6v1',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B6V1 Forms",
        "description": "UDS Initial visiting patients B6V1 forms results pages",
    })
class Ivp_b6v1(Item):
    item_type = 'ivp_b6v1'
    schema = load_schema('encoded:schemas/ivp_b6v1.json')
    embedded = []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
