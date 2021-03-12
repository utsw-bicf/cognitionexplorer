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
    name="concussion_histories",
    unique_key="uuid",
    properties={
        "title": "Local forms-Concussion History",
        "description": "Local form Initial visiting patients Concussion History forms results pages",
    },
)
class Concussion_history(Item):
    item_type = "concussion_history"
    schema = load_schema("encoded:schemas/concussion_history.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []