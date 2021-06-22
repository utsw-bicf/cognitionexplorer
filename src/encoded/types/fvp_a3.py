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
    name="fvp_a3v3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_A3V3 Forms",
        "description": "UDS follow up forms A3V3:Subject Family History results pages",
    },
)
class Fvp_a3v3(Item):
    item_type = "fvp_a3v3"
    schema = load_schema("encoded:schemas/fvp_a3v3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []

@collection(
    name="fvp_a3v2s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_A3V2 Forms",
        "description": "UDS follow up forms A3V2:Subject Family History results pages",
    },
)
class Fvp_a3v2(Item):
    item_type = "fvp_a3v2"
    schema = load_schema("encoded:schemas/fvp_a3v2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []