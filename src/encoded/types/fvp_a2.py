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
    name="fvp_a2",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_A2 Forms",
        "description": "UDS follow-up visiting patients A2 forms results pages",
    },
)
class Fvp_a2(Item):
    item_type = "fvp_a2"
    schema = load_schema("encoded:schemas/fvp_a2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []