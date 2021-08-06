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
    name="fvp_a5v2s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_A5V2 Forms",
        "description": "UDS follow up forms A5V2:Subject Health History results pages",
    },
)
class Fvp_a5v2(Item):
    item_type = "fvp_a5v2"
    schema = load_schema("encoded:schemas/fvp_a5v2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []