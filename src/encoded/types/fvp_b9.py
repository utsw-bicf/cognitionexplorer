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
from pyramid.traversal import find_root, resource_path
from pyramid.security import (
    Allow,
    Deny,
    Everyone,
)

ONLY_ADMIN_VIEW_DETAILS = [
    (Allow, 'group.admin', ['view', 'view_details', 'edit']),
    (Allow, 'group.read-only-admin', ['view', 'view_details']),
    (Allow, 'remoteuser.INDEXER', ['view']),
    (Allow, 'remoteuser.EMBED', ['view']),
    (Deny, Everyone, ['view', 'view_details', 'edit']),
]

USER_ALLOW_CURRENT = [
    (Allow, Everyone, 'view'),
] + ONLY_ADMIN_VIEW_DETAILS

USER_DELETED = [
    (Deny, Everyone, 'visible_for_edit')
] + ONLY_ADMIN_VIEW_DETAILS

@collection(
    name="fvp_b9v3s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B9V3 Forms",
        "description": "UDS follow-up visiting patients B9V3 forms results pages",
    },
)
class Fvp_b9v3(Item):
    item_type = "fvp_b9v3"
    schema = load_schema("encoded:schemas/fvp_b9v3.json")
    embedded = [
    ]
    STATUS_ACL = {
        'released': [(Allow, 'group.verification', ['view_details'])]
    }
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []

@collection(
    name="fvp_b9v2s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B9V2 Forms",
        "description": "UDS follow-up visiting patients B9V2 forms results pages",
    },
)
class Fvp_b9v2(Item):
    item_type = "fvp_b9v2"
    schema = load_schema("encoded:schemas/fvp_b9v2.json")
    embedded = [
    ]
    STATUS_ACL = {
        'released': [(Allow, 'group.verification', ['view_details'])]
    }
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []


@collection(
    name="fvp_b9v1s",
    unique_key="uuid",
    properties={
        "title": "UDS_FVP_B9V1 Forms",
        "description": "UDS follow-up visiting patients B9V1 forms results pages",
    },
)
class Fvp_b9v1(Item):
    item_type = "fvp_b9v1"
    schema = load_schema("encoded:schemas/fvp_b9v1.json")
    embedded = [
    ]
    STATUS_ACL = {
        'released': [(Allow, 'group.verification', ['view_details'])]
    }
    rev = {
    }
    audit_inherit = []
    set_status_up = []
    set_status_down = []