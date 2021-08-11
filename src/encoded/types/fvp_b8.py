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
    name="fvp_b8v3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B8V3 Forms",
        "description": "UDS follow-up visiting patients B8V3 forms results pages",
    },
)
class Fvp_b8v3(Item):
    item_type = "fvp_b8v3"
    schema = load_schema("encoded:schemas/fvp_b8v3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []

@collection(
    name="fvp_b8v2s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B8V2 Forms",
        "description": "UDS follow-up visiting patients B8V2 forms results pages",
    },
)
class Fvp_b8v2(Item):
    item_type = "fvp_b8v2"
    schema = load_schema("encoded:schemas/fvp_b8v2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []


@collection(
    name="fvp_b8v1s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B8V1 Forms",
        "description": "UDS follow-up visiting patients B8V1 forms results pages",
    },
)
class Fvp_b8v1(Item):
    item_type = "fvp_b8v1"
    schema = load_schema("encoded:schemas/fvp_b8v1.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []

    
    