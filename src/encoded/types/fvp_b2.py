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
    name='fvp_b2v2',
    unique_key='uuid',
    properties={
        "title": "UDS_FVP_B2V2 Forms",
        "description": "UDS Follow-up visiting patients B2V2 forms results pages",
    })
class Fvp_b2v2(Item):
    item_type = 'fvp_b2v2'
    schema = load_schema('encoded:schemas/fvp_b2v2.json')
    embedded =  []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []

@collection(
    name='fvp_b2v1',
    unique_key='uuid',
    properties={
        "title": "UDS_FVP_B2V1 Forms",
        "description": "UDS Follow-up visiting patients B2V1 forms results pages",
    })
class Fvp_b2v1(Item):
    item_type = 'fvp_b2v1'
    schema = load_schema('encoded:schemas/fvp_b2v1.json')
    embedded =  []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
