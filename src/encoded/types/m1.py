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
    name="m1s",
    unique_key="uuid",
    properties={
        "title": "UDS_M1 Forms",
        "description": "UDS visiting patients M1 forms results pages",
    },
)
class M1(Item):
    item_type = "m1"
    schema = load_schema("encoded:schemas/m1.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []