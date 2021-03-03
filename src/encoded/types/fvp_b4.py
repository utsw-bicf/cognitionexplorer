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
    name="fvp_b4s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B4 Forms",
        "description": "NACC Uniform Data Set (UDS) - FOLLOW-UP FORM B4: CDR® Dementia Staging Instrument plus NACC FTLD Behavior & Language Domains ( CDR® NACC FTLD)",
    },
)
class Fvp_b4(Item):
    item_type = "fvp_b4"
    schema = load_schema("encoded:schemas/fvp_b4.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []