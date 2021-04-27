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
    name="ivp_d1s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_D1 Forms",
        "description": "UDS Initial visiting patients D1 forms results pages",
    })
class Ivp_d1(Item):
    base_types = ['Ivp_d1'] + Item.base_types
    embedded = [
        
    ]
    rev = {
    }


audit_inherit = []
set_status_up = []
set_status_down = []


@collection(
    name='ivp_d1v3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_D1V3 Forms",
        "description": "UDS Initial visiting patients D1V3 forms results pages",
    })
class Ivp_d1v3(Ivp_d1):
    item_type = 'ivp_d1v3'
    schema = load_schema('encoded:schemas/ivp_d1v3.json')
    embedded = Ivp_d1.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []


@collection(
    name='ivp_d1v2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_D1V2 Forms",
        "description": "UDS Initial visiting patients D1V2 forms results pages",
    })
class Ivp_d1v2(Ivp_d1):
    item_type = 'ivp_d1v2'
    schema = load_schema('encoded:schemas/ivp_d1v2.json')
    embedded = Ivp_d1.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
