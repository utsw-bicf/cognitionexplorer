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
    name="fvp_b1s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B1 Forms",
        "description": "NACC Uniform Data Set (UDS) - FOLLOW-UP FORM B1: EVALUATION FORM - PHYSICAL",
    },
)
class Fvp_b1(Item):
    item_type = "fvp_b1"
    schema = load_schema("encoded:schemas/fvp_b1.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []