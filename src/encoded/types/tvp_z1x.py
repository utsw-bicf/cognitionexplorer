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
    name="tvp_z1xs",
    unique_key="uuid",
    properties={
        "title": "UDS_TVP_Z1X Forms",
        "description": "UDS Telephone follow-up visiting patients Z1X forms results pages",
    },
)
class Tvp_z1x(Item):
    item_type = "tvp_z1x"
    schema = load_schema("encoded:schemas/tvp_z1x.json")
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []