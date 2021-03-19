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
    name="physical_exams",
    unique_key="uuid",
    properties={
        "title": "Physical examination Forms",
        "description": "Local forms Physical examination patients results pages",
    },
)
class Physical_exam(Item):
    item_type = "physical_exam"
    schema = load_schema("encoded:schemas/physical_exam.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []