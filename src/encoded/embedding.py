from copy import deepcopy
from urllib import unquote
from .cache import ManagerLRUCache
from posixpath import join
from pyramid.events import (
    ContextFound,
    subscriber,
)
from pyramid.httpexceptions import HTTPNotFound
from pyramid.url import URLMethodsMixin

def includeme(config):
    config.scan(__name__)
    config.add_request_method(embed, 'embed')
    config.add_request_method(resource_url, 'resource_url')
    config.add_request_method(lambda request: set(), '_embedded_uuids', reify=True)
    config.add_request_method(lambda request: set(), '_linked_uuids', reify=True)


@subscriber(ContextFound)
def add_context_uuid(event):
    request = event.request
    uuid = getattr(request.context, 'uuid', None)
    if uuid is not None:
        request._embedded_uuids.add(str(uuid))


def resource_url(request, resource, *elements, **kw):
    uuid = getattr(resource, 'uuid', None)
    if uuid is not None:
        request._linked_uuids.add(str(uuid))
    return URLMethodsMixin.resource_url(request, resource, *elements, **kw)


def make_subrequest(request, path):
    """ Make a subrequest

    Copies request environ data for authentication.

    May be better to just pull out the resource through traversal and manually
    perform security checks.
    """
    env = request.environ.copy()
    if path and '?' in path:
        path_info, query_string = path.split('?', 1)
        path_info = unquote(path_info)
    else:
        path_info = unquote(path)
        query_string = ''
    env['PATH_INFO'] = path_info
    env['QUERY_STRING'] = query_string
    subreq = request.__class__(env, method='GET', content_type=None,
                               body=b'')
    subreq.remove_conditional_headers()
    # XXX "This does not remove headers like If-Match"
    subreq.__parent__ = request
    return subreq


embed_cache = ManagerLRUCache('embed_cache')


def embed(request, *elements, **kw):
    """ as_user=True for current user
    """
    # Should really be more careful about what gets included instead.
    # Cache cut response time from ~800ms to ~420ms.
    as_user = kw.get('as_user')
    path = join(*elements)
    if isinstance(path, unicode):
        path = path.encode('utf-8')
    if as_user is not None:
        result, embedded, linked = _embed(request, path, as_user)
    else:
        cached = embed_cache.get(path, None)
        if cached is None:
            cached = _embed(request, path)
            embed_cache[path] = cached
        result, embedded, linked = cached
        result = deepcopy(result)
    request._embedded_uuids.update(embedded)
    request._linked_uuids.update(linked)
    return result


def _embed(request, path, as_user='EMBED'):
    subreq = make_subrequest(request, path)
    subreq.override_renderer = 'null_renderer'
    if as_user is not True:
        if 'HTTP_COOKIE' in subreq.environ:
            del subreq.environ['HTTP_COOKIE']
        subreq.remote_user = as_user
    try:
        result = request.invoke_subrequest(subreq)
    except HTTPNotFound:
        raise KeyError(path)
    return result, subreq._embedded_uuids, subreq._linked_uuids


def expand_path(request, obj, path):
    if isinstance(path, basestring):
        path = path.split('.')
    if not path:
        return
    name = path[0]
    remaining = path[1:]
    value = obj.get(name, None)
    if value is None:
        return
    if isinstance(value, list):
        for index, member in enumerate(value):
            if not isinstance(member, dict):
                member = value[index] = request.embed(member, '@@object')
            expand_path(request, member, remaining)
    else:
        if not isinstance(value, dict):
            value = obj[name] = request.embed(value, '@@object')
        expand_path(request, value, remaining)
