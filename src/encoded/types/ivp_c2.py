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
    name="ivp_c2s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_C2 Forms",
        "description": "UDS Initial visiting patients C2 forms results pages",
    },
)
class Ivp_c2(Item):
    item_type = "ivp_c2"
    schema = load_schema("encoded:schemas/ivp_c2.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []