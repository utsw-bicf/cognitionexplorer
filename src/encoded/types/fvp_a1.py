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
    name="fvp_a1v3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_A1V3 Forms",
        "description": "UDS follow up forms A1V3:Subject Demographic results pages",
    },
)
class Fvp_a1v3(Item):
    item_type = "fvp_a1v3"
    schema = load_schema("encoded:schemas/fvp_a1v3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []

@collection(
    name="fvp_a1v2s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_A1V2 Forms",
        "description": "UDS follow up forms A1V2:Subject Demographic results pages",
    },
)
class Fvp_a1v2(Item):
    item_type = "fvp_a1v2"
    schema = load_schema("encoded:schemas/fvp_a1v2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []    

@collection(
    name="fvp_a1v1s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_A1V1 Forms",
        "description": "UDS follow up forms A1V1:Subject Demographic results pages",
    },
)
class Fvp_a1v1(Item):
    item_type = "fvp_a1v1"
    schema = load_schema("encoded:schemas/fvp_a1v1.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []   