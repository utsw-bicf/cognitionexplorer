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
    name="fvp_b6v3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B6 Forms",
        "description": "UDS follow-up visiting patients B6 forms results pages",
    },
)
class Fvp_b6v3(Item):
    item_type = "fvp_b6v3"
    schema = load_schema("encoded:schemas/fvp_b6v3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []