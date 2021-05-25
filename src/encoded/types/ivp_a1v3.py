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
    name="ivp_a1v3s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_A1V3 Forms",
        "description": "UDS initial visits forms A1V3:Subject Demographic results pages",
    },
)
class Ivp_a1v3(Item):
    item_type = "ivp_a1v3"
    schema = load_schema("encoded:schemas/ivp_a1v3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []