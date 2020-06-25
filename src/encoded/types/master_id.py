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
    name="master_id",
    unique_key="ptid",
    properties={
        "title": "Redcap_master_id Forms",
        "description": "Redcap master_id forms: Basic patient information pages",
    },
)
class Master_id(Item):
    item_type = "master_id"
    schema = load_schema("encoded:schemas/master_id.json")
    name_key = 'ptid'
    embedded = [
    ]
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []