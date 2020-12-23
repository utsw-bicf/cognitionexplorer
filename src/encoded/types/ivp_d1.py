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
    name="ivp_d1s",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_D1 Forms",
        "description": "UDS Initial visiting patients D1 forms results pages",
    },
)
class Ivp_d1(Item):
    item_type = "ivp_d1"
    schema = load_schema("encoded:schemas/ivp_d1.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []