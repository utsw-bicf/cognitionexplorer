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
    name="ivp_a1v2s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_A1V2 Forms",
        "description": "UDS follow up forms A1V2:Subject Demographic results pages",
    },
)
class Ivp_a1v2(Item):
    item_type = "ivp_a1v2"
    schema = load_schema("encoded:schemas/ivp_a1v2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []