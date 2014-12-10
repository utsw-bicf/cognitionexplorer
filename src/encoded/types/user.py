from pyramid.view import (
    view_config,
)
from pyramid.security import (
    Allow,
    Deny,
    Everyone,
    effective_principals,
)
from .base import Collection
from ..schema_utils import (
    load_schema,
)
from ..contentbase import (
    Root,
    location,
)
from ..embedding import embed


@location('users')
class User(Collection):
    item_type = 'user'
    unique_key = 'user:email'
    schema = load_schema('user.json')
    properties = {
        'title': 'DCC Users',
        'description': 'Listing of current ENCODE DCC users',
    }

    __acl__ = [
        (Allow, 'group.admin', ['list', 'view_details']),
        (Allow, 'group.read-only-admin', ['list', 'view_details']),
        (Allow, 'role.owner', ['edit', 'view_details']),
        (Allow, 'remoteuser.INDEXER', ['list', 'view']),
        (Allow, Everyone, ['view', 'traverse']),
        (Deny, Everyone, ['list', 'view_details']),
    ]

    class Item(Collection.Item):
        keys = ['email']
        unique_key = 'user.email'
        template = {
            'title': '{first_name} {last_name}',
            '$templated': True,
        }

        def __ac_local_roles__(self):
            owner = 'userid.%s' % self.uuid
            return {owner: 'role.owner'}


@view_config(context=User.Item, permission='view_details', request_method='GET',
             name='details')
@view_config(context=User.Item, permission='view', request_method='GET',
             name='object', additional_permission='view_details')
@view_config(context=User.Item, permission='view', request_method='GET',
             name='page', additional_permission='view_details')
def user_details_view(context, request):
    return context.__json__(request)


@view_config(context=User.Item, permission='view', request_method='GET',
             name='page')
@view_config(context=User.Item, permission='view', request_method='GET',
             name='object')
def user_basic_view(context, request):
    properties = context.__json__(request)
    filtered = {}
    for key in ['@id', '@type', 'uuid', 'lab', 'title']:
        try:
            filtered[key] = properties[key]
        except KeyError:
            pass
    return filtered


@view_config(context=Root, name='current-user', request_method='GET')
def current_user(request):
    request.environ['encoded.canonical_redirect'] = False
    for principal in effective_principals(request):
        if principal.startswith('userid.'):
            break
    else:
        return {}
    namespace, userid = principal.split('.', 1)
    collection = request.root.by_item_type[User.item_type]
    path = request.resource_path(collection, userid, '@@details')
    return embed(request, path, as_user=True)
