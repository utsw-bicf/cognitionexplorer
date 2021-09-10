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
    name="fvp_d2v3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_D2 Forms",
        "description": "UDS follow-up visiting patients D2 forms results pages",
    },
)
class Fvp_d2v3(Item):
    item_type = "fvp_d2v3"
    schema = load_schema("encoded:schemas/fvp_d2v3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []