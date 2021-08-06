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
    name='fvp_e1v2',
    unique_key='uuid',
    properties={
        "title": "UDS_FVP_E1V2 Forms",
        "description": "UDS Follow-up visiting patients E1V2 forms results pages",
    })
class Fvp_e1v2(Item):
    item_type = 'fvp_e1v2'
    schema = load_schema('encoded:schemas/fvp_e1v2.json')
    embedded =  []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
