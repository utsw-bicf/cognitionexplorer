from ..schema_utils import (
    load_schema,
)
from ..contentbase import (
    location,
)
from .base import (
    Item,
)
from .download import ItemWithAttachment


@location(
    name='images',
    unique_key='image:filename',
    properties={
        'title': 'Image',
        'description': 'Listing of portal images',
    })
class Image(ItemWithAttachment, Item):
    item_type = 'image'
    schema = load_schema('image.json')
    schema['properties']['attachment']['properties']['type']['enum'] = [
        'image/png',
        'image/jpeg',
        'image/gif',
    ]
    embedded = ['submitted_by']

    def keys(self):
        keys = super(Image, self).keys()
        properties = self.upgrade_properties(finalize=False)
        value = properties['attachment']['download']
        keys.setdefault('image:filename', []).append(value)
        return keys
