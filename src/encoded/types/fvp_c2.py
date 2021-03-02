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
    name="fvp_c2s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_A2 Forms",
        "description": "UDS follow-up visiting patients A2 forms results pages",
    },
)
class Fvp_c2(Item):
    item_type = "fvp_c2"
    schema = load_schema("encoded:schemas/fvp_c2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []