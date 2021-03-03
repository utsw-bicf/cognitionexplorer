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
    name="ivp_a3s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_A3 Forms",
        "description": "UDS Initial visiting patients A3 forms results pages",
    },
)
class Ivp_a3(Item):
    item_type = "ivp_a3"
    schema = load_schema("encoded:schemas/ivp_a3.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []