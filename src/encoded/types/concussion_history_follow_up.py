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
    name="concussion_histories_follow_up",
    unique_key="uuid",
    properties={
        "title": "Local forms-Concussion History Follow Up Form",
        "description": "Local form Initial visiting patients Concussion History follow up forms results pages",
    },
)
class Concussion_history_follow_up(Item):
    item_type = "concussion_history_follow_up"
    schema = load_schema("encoded:schemas/concussion_history_follow_up.json")
    embedded = [
       
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []