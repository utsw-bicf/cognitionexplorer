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
    name="ivp_b6s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_B6 Forms",
        "description": "UDS Initial visiting patients B6 forms results pages",
    },
)
class Ivp_b6(Item):
    item_type = "ivp_b6"
    schema = load_schema("encoded:schemas/ivp_b6.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []