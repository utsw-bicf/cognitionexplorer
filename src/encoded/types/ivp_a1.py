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
    name="ivp_a1",
    unique_key="uuid",
    properties={
        "title": "UDS_IVP_A1 Forms",
        "description": "UDS Initial visiting patients A1 forms results pages",
    },
)
class Ivp_a1(Item):
    item_type = "ivp_a1"
    schema = load_schema("encoded:schemas/ivp_a1.json")
    # name_key = "uuid"
    embedded = [
        # "ihc",
    ]
    rev = {
        # "ihc": ("Ihc", "pathology_report"),
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []