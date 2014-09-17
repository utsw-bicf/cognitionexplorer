from ..schema_utils import (
    load_schema,
)
from ..contentbase import (
    location,
)
from .base import (
    ALIAS_KEYS,
    Collection,
)
from .download import ItemWithAttachment


class Characterization(Collection):
    class Item(ItemWithAttachment, Collection.Item):
        base_types = ['characterization'] + Collection.Item.base_types
        embedded = set(['lab', 'award', 'submitted_by'])
        keys = ALIAS_KEYS


@location('construct-characterizations')
class ConstructCharacterization(Characterization):
    item_type = 'construct_characterization'
    schema = load_schema('construct_characterization.json')
    properties = {
        'title': 'Construct characterizations',
        'description': 'Listing of biosample construct characterizations',
    }


@location('rnai-characterizations')
class RNAiCharacterization(Characterization):
    item_type = 'rnai_characterization'
    schema = load_schema('rnai_characterization.json')
    properties = {
        'title': 'RNAi characterizations',
        'description': 'Listing of biosample RNAi characterizations',
    }


@location('donor-characterizations')
class DonorCharacterization(Characterization):
    item_type = 'donor_characterization'
    schema = load_schema('donor_characterization.json')
    properties = {
        'title': 'Donor characterizations',
        'description': 'Listing of model organism donor (strain) construct characterizations',
    }


@location('biosample-characterizations')
class BiosampleCharacterization(Characterization):
    item_type = 'biosample_characterization'
    schema = load_schema('biosample_characterization.json')
    properties = {
        'title': 'Biosample characterizations',
        'description': 'Listing of biosample characterizations',
    }


@location('antibody-characterizations')
class AntibodyCharacterization(Characterization):
    item_type = 'antibody_characterization'
    schema = load_schema('antibody_characterization.json')
    properties = {
        'title': 'Antibody characterizations',
        'description': 'Listing of antibody characterization documents',
    }

    class Item(Characterization.Item):
        embedded = [
            'submitted_by',
            'lab',
            'award',
            'target',
            'target.organism',
            'documents',
            'characterizes.targets',
        ]

        template = {
            'characterization_method': {
                '$value': '{characterization_method}',
                '$templated': True,
                '$condition': 'characterization_method',
            },
        }

        def template_namespace(self, properties, request=None):
            ns = Collection.Item.template_namespace(self, properties, request)
            if request is None:
                return ns
            if 'primary_characterization_method' in ns:
                ns['characterization_method'] = ns['primary_characterization_method']
            elif 'secondary_characterization_method' in ns:
                ns['characterization_method'] = ns['secondary_characterization_method']
            else:
                ns['characterization_method'] = ''
            return ns
