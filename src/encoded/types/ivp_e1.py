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
    name='ivp_e1v2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_E1V2 Forms",
        "description": "UDS Initial visiting patients E1V2 forms results pages",
    })
class Ivp_e1v2(Item):
    item_type = 'ivp_e1v2'
    schema = load_schema('encoded:schemas/ivp_e1v2.json')
    embedded =  []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
