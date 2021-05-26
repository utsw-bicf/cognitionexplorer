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
    name="fvp_z1xv3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_Z1X Forms",
        "description": "UDS follow-up visiting patients Z1X forms results pages",
    },
)
class Fvp_z1xv3(Item):
    item_type = "fvp_z1xv3"
    schema = load_schema("encoded:schemas/fvp_z1xv3.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []