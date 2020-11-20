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
    name="fvp_b7s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B7 Forms",
        "description": "UDS follow-up visiting patients B7 forms results pages",
    },
)
class Fvp_b7(Item):
    item_type = "fvp_b7"
    schema = load_schema("encoded:schemas/fvp_b7.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []