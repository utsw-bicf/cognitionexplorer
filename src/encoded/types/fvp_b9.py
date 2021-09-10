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
    name="fvp_b9v3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B9V3 Forms",
        "description": "UDS follow-up visiting patients B9V3 forms results pages",
    },
)
class Fvp_b9v3(Item):
    item_type = "fvp_b9v3"
    schema = load_schema("encoded:schemas/fvp_b9v3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []

@collection(
    name="fvp_b9v2s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B9V2 Forms",
        "description": "UDS follow-up visiting patients B9V2 forms results pages",
    },
)
class Fvp_b9v2(Item):
    item_type = "fvp_b9v2"
    schema = load_schema("encoded:schemas/fvp_b9v2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []


@collection(
    name="fvp_b9v1s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B9V1 Forms",
        "description": "UDS follow-up visiting patients B9V1 forms results pages",
    },
)
class Fvp_b9v1(Item):
    item_type = "fvp_b9v1"
    schema = load_schema("encoded:schemas/fvp_b9v1.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []