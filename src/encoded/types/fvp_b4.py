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
    name="fvp_b4v3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B4V3 Forms",
        "description": "NACC Uniform Data Set (UDS) - FOLLOW-UP FORM B4V3: CDR® Dementia Staging Instrument plus NACC FTLD Behavior & Language Domains ( CDR® NACC FTLD)",
    },
)
class Fvp_b4v3(Item):
    item_type = "fvp_b4v3"
    schema = load_schema("encoded:schemas/fvp_b4v3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []

@collection(
    name="fvp_b4v2s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B4V2 Forms",
        "description": "NACC Uniform Data Set (UDS) - FOLLOW-UP FORM B4V2: CDR® Dementia Staging Instrument plus NACC FTLD Behavior & Language Domains ( CDR® NACC FTLD)",
    },
)
class Fvp_b4v2(Item):
    item_type = "fvp_b4v2"
    schema = load_schema("encoded:schemas/fvp_b4v2.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []