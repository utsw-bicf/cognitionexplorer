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
    name="fvp_a2v3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_A2V3 Forms",
        "description": "UDS follow-up visiting patients A2V3 forms results pages",
    },
)
class Fvp_a2v3(Item):
    item_type = "fvp_a2v3"
    schema = load_schema("encoded:schemas/fvp_a2v3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []

@collection(
    name="fvp_a2v2s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_A2V2 Forms",
        "description": "UDS follow-up visiting patients A2V2 forms results pages",
    },
)
class Fvp_a2v2(Item):
    item_type = "fvp_a2v2"
    schema = load_schema("encoded:schemas/fvp_a2v2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []


@collection(
    name="fvp_a2v1s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_A2V1 Forms",
        "description": "UDS follow-up visiting patients A2V1 forms results pages",
    },
)
class Fvp_a2v1(Item):
    item_type = "fvp_a2v1"
    schema = load_schema("encoded:schemas/fvp_a2v1.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []