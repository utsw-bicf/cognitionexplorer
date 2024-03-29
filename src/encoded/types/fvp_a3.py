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
    name="fvp_a3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_a3 Forms",
        "description": "UDS follow up forms a3:Subject Demographic results pages",
    },
)
class Fvp_a3(Item):
    item_type = "fvp_a3"
    schema = load_schema("encoded:schemas/fvp_a3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []