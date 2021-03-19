from snovault import (
    calculated_property,
    collection,
    load_schema,
)
# from snovault.util import Path
from pyramid.security import Authenticated
from .base import (
    Item,
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
    name='ivp_b2v2',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B2V2 Forms",
        "description": "UDS Initial visiting patients B2V2 forms results pages",
    })
class Ivp_b2v2(Item):
    item_type = 'ivp_b2v2'
    schema = load_schema('encoded:schemas/ivp_b2v2.json')
    embedded =  []
    STATUS_ACL = {
        'released': [(Allow, 'group.verification', ['view_details'])]
    }
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []

@collection(
    name='ivp_b2v1',
    unique_key='uuid',
    properties={
        "title": "UDS_IVP_B2V1 Forms",
        "description": "UDS Initial visiting patients B2V1 forms results pages",
    })
class Ivp_b2v1(Item):
    item_type = 'ivp_b2v1'
    schema = load_schema('encoded:schemas/ivp_b2v1.json')
    embedded =  []
    STATUS_ACL = {
        'released': [(Allow, 'group.verification', ['view_details'])]
    }
    rev = {
    }
    audit_inherit = []
    set_status_up = [

    ]
    set_status_down = []