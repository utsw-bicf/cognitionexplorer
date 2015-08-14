from base64 import b64decode
from io import BytesIO
from mimetypes import guess_type
from PIL import Image
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPTemporaryRedirect,
)
from pyramid.response import Response
from pyramid.settings import asbool
from pyramid.traversal import find_root
from pyramid.view import view_config
from urllib.parse import (
    parse_qs,
    quote,
    unquote,
    urlparse,
)
from contentbase import (
    BLOBS,
    Item,
)
from .validation import ValidationFailure
import datetime
import magic
import mimetypes
import pytz


def includeme(config):
    config.scan(__name__)


def parse_data_uri(uri):
    if not uri.startswith('data:'):
        raise ValueError(uri)
    meta, data = uri[len('data:'):].split(',', 1)
    meta = meta.split(';')
    mime_type = meta[0] or None
    charset = None
    is_base64 = False
    for part in meta[1:]:
        if part == 'base64':
            is_base64 = True
            continue
        if part.startswith('charset='):
            charset = part[len('charset='):]
            continue
        raise ValueError(uri)

    if is_base64:
        data = b64decode(data)
    else:
        data = unquote(data)

    return mime_type, charset, data


def mimetypes_are_equal(m1, m2):
    major1 = m1.split('/')[0]
    major2 = m2.split('/')[0]
    if major1 == 'text' and major2 == 'text':
        return True
    return m1 == m2


class ItemWithAttachment(Item):
    """ Item base class with attachment blob
    """
    download_property = 'attachment'

    def _process_downloads(self, properties, sheets):
        prop_name = self.download_property
        attachment = properties[prop_name]
        href = attachment['href']

        if not href.startswith('data:'):
            msg = "Expected data URI."
            raise ValidationFailure('body', [prop_name, 'href'], msg)

        properties = properties.copy()
        properties[prop_name] = attachment = attachment.copy()

        if sheets is None:
            sheets = {}
        else:
            sheets = sheets.copy()
        sheets['downloads'] = downloads = {}
        download_meta = downloads[prop_name] = {}

        try:
            mime_type, charset, data = parse_data_uri(href)
        except (ValueError, TypeError):
            msg = 'Could not parse data URI.'
            raise ValidationFailure('body', [prop_name, 'href'], msg)
        if charset is not None:
            download_meta['charset'] = charset

        # Make sure the file extensions matches the mimetype
        download_meta['download'] = filename = attachment['download']
        mime_type_from_filename, _ = mimetypes.guess_type(filename)
        if mime_type_from_filename is None:
            mime_type_from_filename = 'application/octet-stream'
        if mime_type:
            if not mimetypes_are_equal(mime_type, mime_type_from_filename):
                raise ValidationFailure(
                    'body', [prop_name, 'href'],
                    'Wrong file extension for %s mimetype.' % mime_type)
        else:
            mime_type = mime_type_from_filename

        # Make sure the mimetype appears to be what the client says it is
        mime_type_detected = magic.from_buffer(data, mime=True).decode('utf-8')
        if not mimetypes_are_equal(mime_type, mime_type_detected):
            msg = "Incorrect file type. (Appears to be %s)" % mime_type_detected
            raise ValidationFailure('body', [prop_name, 'href'], msg)

        attachment['type'] = mime_type
        if mime_type is not None:
            download_meta['type'] = mime_type

        # Make sure mimetype is not disallowed
        try:
            allowed_types = self.schema['properties'][prop_name]['properties']['type']['enum']
        except KeyError:
            pass
        else:
            if mime_type not in allowed_types:
                raise ValidationFailure(
                    'body', [prop_name, 'href'], 'Mimetype %s is not allowed.' % mime_type)

        # Validate images and store height/width
        major, minor = mime_type.split('/')
        if major == 'image' and minor in ('png', 'jpeg', 'gif', 'tiff'):
            stream = BytesIO(data)
            im = Image.open(stream)
            im.verify()
            attachment['width'], attachment['height'] = im.size

        registry = find_root(self).registry
        registry[BLOBS].store_blob(data, download_meta)

        attachment['href'] = '@@download/%s/%s' % (
            prop_name, quote(filename))

        return properties, sheets

    def _update(self, properties, sheets=None):
        prop_name = self.download_property
        attachment = properties.get(prop_name, {})
        href = attachment.get('href', None)
        if href is not None:
            if href.startswith('@@download/'):
                try:
                    existing = self.properties[prop_name]['href']
                except KeyError:
                    existing = None
                if existing != href:
                    msg = "Expected data uri or existing uri."
                    raise ValidationFailure('body', [prop_name, 'href'], msg)
            else:
                properties, sheets = self._process_downloads(properties, sheets)

        super(ItemWithAttachment, self)._update(properties, sheets)


@view_config(name='download', context=ItemWithAttachment, request_method='GET',
             permission='view', subpath_segments=2)
def download(context, request):
    prop_name, filename = request.subpath
    downloads = context.propsheets['downloads']
    try:
        download_meta = downloads[prop_name]
    except KeyError:
        raise HTTPNotFound(prop_name)

    if download_meta['download'] != filename:
        raise HTTPNotFound(filename)

    mimetype, content_encoding = guess_type(filename, strict=False)
    if mimetype is None:
        mimetype = 'application/octet-stream'

    # If blob is external, serve via proxy using X-Accel-Redirect
    blob_storage = request.registry[BLOBS]
    if hasattr(blob_storage, 'get_blob_url'):
        blob_url = blob_storage.get_blob_url(download_meta)
        if blob_url is not None:
            return Response(headers={'X-Accel-Redirect': '/_proxy/' + str(blob_url)})

    # Otherwise serve the blob data ourselves
    blob = request.registry[BLOBS].get_blob(download_meta)
    headers = {
        'Content-Type': mimetype,
    }
    return Response(body=blob, headers=headers)
