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
    name="updrses",
    unique_key="uuid",
    properties={
        "title": "UPDRS Forms",
        "description": "Local forms UPDRS patients results pages",
    },
)
class Updrs(Item):
    item_type = "updrs"
    schema = load_schema("encoded:schemas/updrs.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []