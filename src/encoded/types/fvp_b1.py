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
    name="fvp_b1v3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B1V3 Forms",
        "description": "NACC Uniform Data Set (UDS) - FOLLOW-UP FORM B1V3: EVALUATION FORM - PHYSICAL",
    },
)
class Fvp_b1v3(Item):
    item_type = "fvp_b1v3"
    schema = load_schema("encoded:schemas/fvp_b1v3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []


@collection(
    name="fvp_b1v2s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B1V2 Forms",
        "description": "NACC Uniform Data Set (UDS) - FOLLOW-UP FORM B1V2: EVALUATION FORM - PHYSICAL",
    },
)
class Fvp_b1v2(Item):
    item_type = "fvp_b1v2"
    schema = load_schema("encoded:schemas/fvp_b1v2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []

@collection(
    name="fvp_b1v1s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B1V1 Forms",
        "description": "NACC Uniform Data Set (UDS) - FOLLOW-UP FORM B1V1: EVALUATION FORM - PHYSICAL",
    },
)
class Fvp_b1v1(Item):
    item_type = "fvp_b1v1"
    schema = load_schema("encoded:schemas/fvp_b1v1.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []