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
    name="ivp_z1xs",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_Z1X Forms",
        "description": "UDS Initial visiting patients Z1X forms results pages",
    })
class Ivp_z1x(Item):
    base_types = ['Ivp_z1x'] + Item.base_types
    embedded = [
        
    ]
    rev = {
    }


audit_inherit = []
set_status_up = []
set_status_down = []


@collection(
    name='ivp_z1xv3',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_Z1XV3 Forms",
        "description": "UDS Initial visiting patients Z1XV3 forms results pages",
    })
class Ivp_z1xv3(Ivp_z1x):
    item_type = 'ivp_z1xv3'
    schema = load_schema('encoded:schemas/ivp_z1xv3.json')
    embedded = Ivp_z1x.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []


@collection(
    name='ivp_z1xv2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_Z1XV2 Forms",
        "description": "UDS Initial visiting patients Z1XV2 forms results pages",
    })
class Ivp_z1xv2(Ivp_z1x):
    item_type = 'ivp_z1xv2'
    schema = load_schema('encoded:schemas/ivp_z1xv2.json')
    embedded = Ivp_z1x.embedded + []
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []
