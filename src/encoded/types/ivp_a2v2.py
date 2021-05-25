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
    name="ivp_a2v2s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_A2V2 Forms",
        "description": "UDS initial visits forms A2V2:Informant Demographics results pages",
    },
)
class Ivp_a2v2(Item):
    item_type = "ivp_a2v2"
    schema = load_schema("encoded:schemas/ivp_a2v2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []