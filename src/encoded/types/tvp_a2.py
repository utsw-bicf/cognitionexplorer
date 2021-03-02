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
    name="tvp_a2s",
    unique_key="uuid",
    properties={
        "title": "UDS_TVP_A2 Forms",
        "description": "UDS Telephone follow-up visiting patients A2 forms results pages",
    },
)
class Tvp_a2(Item):
    item_type = "tvp_a2"
    schema = load_schema("encoded:schemas/tvp_a2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []