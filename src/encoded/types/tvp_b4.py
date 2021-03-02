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
    name="tvp_b4s",
    unique_key="uuid",
    properties={
        "title": "UDS_TVP_A1 Forms",
        "description": "UDS Telephone follow-up visiting patients A1 forms results pages",
    },
)
class Tvp_b4(Item):
    item_type = "tvp_b4"
    schema = load_schema("encoded:schemas/tvp_b4.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []