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
    name="visit_contacts",
    unique_key="uuid",
    properties={
        "title": "Visit/Contact Forms",
        "description": "Local forms Visit/Contact patients results pages",
    },
)
class Visit_contact(Item):
    item_type = "visit_contact"
    schema = load_schema("encoded:schemas/visit_contact.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []