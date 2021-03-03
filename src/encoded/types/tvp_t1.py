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
    name="tvp_t1s",
    unique_key="uuid",
    properties={
        "title": "UDS_TVP_T1 Forms",
        "description": "UDS Telephone follow-up visiting patients T1 forms results pages",
    },
)
class Tvp_t1(Item):
    item_type = "tvp_t1"
    schema = load_schema("encoded:schemas/tvp_t1.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []