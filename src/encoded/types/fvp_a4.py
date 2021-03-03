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
    name="fvp_a4s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_a4 Forms",
        "description": "UDS follow up forms a4:Subject Demographic results pages",
    },
)
class Fvp_a4(Item):
    item_type = "fvp_a4"
    schema = load_schema("encoded:schemas/fvp_a4.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []