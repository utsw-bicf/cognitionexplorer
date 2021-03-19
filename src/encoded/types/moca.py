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
    name="mocas",
    unique_key="uuid",
    properties={
        "title": "Local_form MoCA Forms",
        "description": "Local form visiting patients MoCA forms results pages",
    },
)
class Moca(Item):
    item_type = "moca"
    schema = load_schema("encoded:schemas/moca.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []