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
    name="ivp_b1s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_B1 Forms",
        "description": "UDS Initial visiting patients B1 forms results pages",
    },
)
class Ivp_b1(Item):
    item_type = "ivp_b1"
    schema = load_schema("encoded:schemas/ivp_b1.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []