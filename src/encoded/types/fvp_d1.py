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
    name="fvp_d1s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_D1 Forms",
        "description": "UDS follow-up visiting patients D1 forms results pages",
    },
)
class Fvp_d1(Item):
    item_type = "fvp_d1"
    schema = load_schema("encoded:schemas/fvp_d1.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []