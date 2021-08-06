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
    name="fvp_d1v3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_D1V3 Forms",
        "description": "UDS follow-up visiting patients D1V3 forms results pages",
    },
)
class Fvp_d1v3(Item):
    item_type = "fvp_d1v3"
    schema = load_schema("encoded:schemas/fvp_d1v3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []

@collection(
    name="fvp_d1v2s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_D1V2 Forms",
        "description": "UDS follow-up visiting patients D1V2 forms results pages",
    },
)
class Fvp_d1v2(Item):
    item_type = "fvp_d1v2"
    schema = load_schema("encoded:schemas/fvp_d1v2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []