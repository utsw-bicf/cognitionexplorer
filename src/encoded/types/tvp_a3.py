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
    name="tvp_a3s",
    unique_key="uuid",
    properties={
        "title": "UDS_TVP_a3 Forms",
        "description": "UDS Telephone follow-up visiting patients a3 forms results pages",
    },
)
class Tvp_a3(Item):
    item_type = "tvp_a3"
    schema = load_schema("encoded:schemas/tvp_a3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []