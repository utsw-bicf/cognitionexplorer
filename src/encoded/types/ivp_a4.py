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
    name="ivp_a4s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_a4 Forms",
        "description": "UDS Initial visiting patients a4 forms results pages",
    },
)
class Ivp_a4(Item):
    item_type = "ivp_a4"
    schema = load_schema("encoded:schemas/ivp_a4.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []