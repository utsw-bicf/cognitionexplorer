from snovault import (
    calculated_property,
    collection,
    load_schema,
)
from .base import (
    Item,
    # SharedItem,
    paths_filtered_by_status,
)
import re



@collection(
    name='ivp_b1v3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B1V3 Forms",
        "description": "UDS Initial visiting patients B1V3 forms results pages",
    })
class Ivp_b1v3(Item):
    item_type = 'ivp_b1v3'
    schema = load_schema('encoded:schemas/ivp_b1v3.json')
    embedded = []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []


@collection(
    name='ivp_b1v2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B1V2 Forms",
        "description": "UDS Initial visiting patients B1V2 forms results pages",
    })
class Ivp_b1v2(Item):
    item_type = 'ivp_b1v2'
    schema = load_schema('encoded:schemas/ivp_b1v2.json')
    embedded = []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []

@collection(
    name='ivp_b1v1',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B1V1 Forms",
        "description": "UDS Initial visiting patients B1V1 forms results pages",
    })
class Ivp_b1v1(Item):
    item_type = 'ivp_b1v1'
    schema = load_schema('encoded:schemas/ivp_b1v1.json')
    embedded = []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
