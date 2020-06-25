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
    unique_key="uuid",
    properties={
        "title": "Redcap_master_id Forms",
        "description": "Redcap master_id forms: Basic patient information pages",
    },
)
class Master_id(Item):
    item_type = "master_id"
    schema = load_schema("encoded:schemas/master_id.json")
    name_key ='uuid'
    embedded = [
        'ivp_a1'
    ]
    rev = {
        'ivp_a1': ('Ivp_a1', 'master_id'),
    }

    audit_inherit = []
    set_status_up = []
    set_status_down = []

    @calculated_property(schema={
        "title": "Ivp_a1",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a1"
        },
    })
    def ivp_a1(self, request, ivp_a1):
        return paths_filtered_by_status(request, ivp_a1)