from pyramid.view import (
    view_config,
)
from pyramid.security import (
    Allow,
    Deny,
    Everyone,
)
from pyramid.traversal import find_root
from snovault import (
    calculated_property,
    collection,
    load_schema,
)
from .base import (
    Item,
    SharedItem,
    paths_filtered_by_status,
)
# from .histology_filters import histology_filters
from snovault.resource_views import item_view_object
from snovault.util import expand_path
from collections import defaultdict
from datetime import datetime
import math


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
     name='patients',
     unique_key='accession',
     properties={
         'title': 'Patients',
         'description': 'Listing Patients',
     })
class Patient(Item):
    item_type = 'patient'
    schema = load_schema('encoded:schemas/patient.json')
    name_key = 'accession'
    embedded = [
        'ivp_a1v3',
        'fvp_a1v3',
        
        ]
    rev = {
         'ivp_a1v3': ('Ivp_a1v3', 'patient'),
         'fvp_a1v3': ('Fvp_a1v3', 'patient'),
       
    }
    set_status_up = [
      


    ]
    set_status_down = []
    STATUS_ACL = {
        'released': [(Allow, 'group.verification', ['view'])] + USER_ALLOW_CURRENT
    }


    @calculated_property(schema={
        "title": "Ivp_a1v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Ivp_a1v3"
        },
    })
    def ivp_a1v3(self, request, ivp_a1v3):
        return paths_filtered_by_status(request, ivp_a1v3)


    @calculated_property(schema={
        "title": "Fvp_a1v3",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Fvp_a1v3"
        },
    })
    def fvp_a1v3(self, request, fvp_a1v3):
        return paths_filtered_by_status(request, fvp_a1v3)
    
    # @property
    # def __name__(self):
    #     return self.name()


    # @view_config(context=Patient, permission='view', request_method='GET', name='page')
    
    # def patient_page_view(context, request):
    #     if request.has_permission('view_details'):
    #         properties = item_view_object(context, request)
    #     else:
    #         item_path = request.resource_path(context)
    #         properties = request.embed(item_path, '@@object')
    #     for path in context.embedded:
    #         expand_path(request, properties, path)
    #     return properties


    # @view_config(context=Patient, permission='view', request_method='GET',name='object')

    # def patient_basic_view(context, request):
    #     properties = item_view_object(context, request)
    #     filtered = {}
    #     for key in ['@id', '@type', 'accession', 'uuid', 'ivp_a1v3','fvp_a1v3']:
    #         try:
    #             filtered[key] = properties[key]
    #         except KeyError:
    #             pass
    #     return filtered