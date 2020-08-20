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
    name="fvp_a1s",
    # unique_key="master_id",
    properties={
        "title": "UDS_FVP_A1 Forms",
        "description": "UDS follow up forms A1:Subject Demographic results pages",
    },
)
class Fvp_a1(Item):
    item_type = "fvp_a1"
    schema = load_schema("encoded:schemas/fvp_a1.json")
    # name_key = 'ptid'
    embedded = [
        # "ptid"
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []