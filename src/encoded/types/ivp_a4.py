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
    name='ivp_a4v3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_A4V3 Forms",
        "description": "UDS Initial visiting patients A4V3 forms results pages",
    })
class Ivp_a4v3(Item):
    item_type = 'ivp_a4v3'
    schema = load_schema('encoded:schemas/ivp_a4v3.json')
    embedded = []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []


@collection(
    name='ivp_a4v2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_A4V2 Forms",
        "description": "UDS Initial visiting patients A4V2 forms results pages",
    })
class Ivp_a4v2(Item):
    item_type = 'ivp_a4v2'
    schema = load_schema('encoded:schemas/ivp_a4v2.json')
    embedded = []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
