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
    name="tvp_d2s",
    unique_key="uuid",
    properties={
        "title": "UDS_TVP_D2 Forms",
        "description": "UDS Telephone follow-up visiting patients D2 forms results pages",
    },
)
class Tvp_d2(Item):
    item_type = "tvp_d2"
    schema = load_schema("encoded:schemas/tvp_d2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []