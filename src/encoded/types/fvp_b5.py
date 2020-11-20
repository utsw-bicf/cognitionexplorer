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
    name="fvp_b5s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B5 Forms",
        "description": "UDS follow-up visiting patients B5 forms results pages",
    },
)
class Fvp_b5(Item):
    item_type = "fvp_b5"
    schema = load_schema("encoded:schemas/fvp_b5.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []