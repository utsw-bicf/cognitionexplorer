import re
from pyramid.view import view_config
from ..contentbase import TYPES
from ..indexing import ELASTIC_SEARCH
from pyramid.security import effective_principals
from urllib.parse import urlencode
from collections import OrderedDict
import requests

sanitize_search_string_re = re.compile(r'[\\\+\-\&\|\!\(\)\{\}\[\]\^\~\:\/\\\*\?]')
extra_params = [
    'type',
    'limit',
    'mode',
    'format',
    'frame',
    'datastore',
    'regionid',
    'annotation',
]
ENSEMBL_URL = 'http://rest.ensembl.org/'

hgConnect = ''.join([
    'http://genome.ucsc.edu/cgi-bin/hgHubConnect',
    '?hgHub_do_redirect=on',
    '&hgHubConnect.remakeTrackHub=on',
    '&hgHub_do_firstDb=1',
    '&hubUrl=',
])

audit_facets = [
    ('audit.ERROR.category', {'title': 'Audit category: ERROR'}),
    ('audit.NOT_COMPLIANT.category', {'title': 'Audit category: NOT COMPLIANT'}),
    ('audit.WARNING.category', {'title': 'Audit category: WARNING'}),
    ('audit.DCC_ACTION.category', {'title': 'Audit category: DCC ACTION'})
]


def get_filtered_query(term, fields, principals):
    return {
        'query': {
            'query_string': {
                'query': term,
                'default_operator': 'AND',
                'fields': [
                    'encoded_all_ngram',
                    'encoded_all_standard',
                    'encoded_all_untouched'],
                'analyzer': 'encoded_search_analyzer'
            }
        },
        'filter': {
            'and': {
                'filters': [
                    {
                        'terms': {
                            'principals_allowed.view': principals
                        }
                    }
                ]
            }
        },
        'highlight': {
            'fields': {
                '_all': {}
            }
        },
        'aggs': {},
        '_source': list(fields),
    }


def sanitize_search_string(text):
    return sanitize_search_string_re.sub(r'\\\g<0>', text)


def assembly_mapper(location, species, old_assembly, new_assembly):
    # All others
    new_url = ENSEMBL_URL + 'map/' + species + '/' \
        + new_assembly + '/' + location + '/' + old_assembly \
        + '/?content-type=application/json'
    try:
        new_response = requests.get(new_url).json()
    except:
        return('', '', '')
    else:
        data = new_response['mappings'][0]['mapped']
        chromosome = 'chr' + data['seq_region_name']
        start = data['start']
        end = data['end']
        return(chromosome, start, end)


def search_peaks(request):
    """
    return file uuids which have the snp or interval found in given region
    """
    es = request.registry[ELASTIC_SEARCH]
    peakid = request.params.get('regionid', None).lower()

    assembly = 'hg19'
    old_assembly = 'GRCh37'
    new_assembly = 'GRCh38'

    if request.params.get('annotation', '') != 'hg19':
        assembly = 'mm9'
        species = 'mouse'
        old_assembly = 'NCBIM37'
        new_assembly = 'GRCm38'
    chromosome = ''
    start = ''
    end = ''

    if peakid.startswith('rs'):
        # RSIDs should be handled here
        url = ENSEMBL_URL + 'variation/' + species + '/' + peakid \
            + '/?content-type=application/json'
        try:
            response = requests.get(url).json()
        except:
            return([], 'Failed search')
        else:
            if 'mappings' in response:
                location = response['mappings'][0]['location']
                chromosome, start, end = assembly_mapper(location,
                                                         species,
                                                         old_assembly,
                                                         new_assembly)
    elif peakid.startswith('chr'):
        # Address should be handled here
        params = peakid.split('-')
        chromosome = params[0]
        start = params[1]
        end = params[1]
        if len(params) > 2:
            end = params[2]
    else:
        try:
            url = 'http://www.mygene.info/v2/gene/' \
                + peakid + '?fields=genomic_pos,genomic_pos_hg19'
            response = requests.get(url).json()
        except:
            return([], 'Failed search')
        else:
            if 'genomic_pos_hg19' in response:
                # Human assemgly since we have hg19
                chromosome = 'chr' + response['genomic_pos_hg19']['chr']
                start = response['genomic_pos_hg19']['start']
                end = response['genomic_pos_hg19']['end']
            elif 'genomic_pos_mm9' in response:
                # mouse assemble since we have mm9
                chromosome = 'chr' + response['genomic_pos_mm9']['chr']
                start = response['genomic_pos_mm9']['start']
                end = response['genomic_pos_mm9']['end']
            elif 'genomic_pos' in response:
                # All others
                location = response['genomic_pos']['chr'] \
                    + ':' + str(response['genomic_pos']['start']) \
                    + '-' + str(response['genomic_pos']['end'])
                chromosome, start, end = assembly_mapper(location, species, old_assembly, new_assembly)
            else:
                return([], 'Failed search')

    file_ids = []
    if chromosome == '' or start == '':
        notification = 'Invalid entry'
        return (file_ids, notification)
    else:
        query = {
            'query': {
                'filtered': {
                    'query': {
                        'term': {
                            'chromosome': chromosome
                        }
                    },
                    'filter': {
                        'and': {
                            'filters': [
                                {
                                    'range': {
                                        'start': {
                                            'lte': end,
                                        }
                                    }
                                },
                                {
                                    'range': {
                                        'stop': {
                                            'gte': start
                                        }
                                    }
                                }
                            ],
                            '_cache': True
                        }
                    }
                }
            },
            'fields': ['uuid']
        }
        results = es.search(body=query, index='peaks', doc_type=assembly or None, size=99999999)
        for hit in results['hits']['hits']:
            if hit['fields']['uuid'] not in file_ids:
                file_ids.append(hit['fields']['uuid'][0])
        return (file_ids, 'success')


@view_config(route_name='search', request_method='GET', permission='search')
def search(context, request, search_type=None):
    ''' Search view connects to ElasticSearch and returns the results'''

    root = request.root
    types = request.registry[TYPES]
    result = {
        '@id': '/search/' + ('?' + request.query_string if request.query_string else ''),
        '@type': ['search'],
        'title': 'Search',
        'facets': [],
        '@graph': [],
        'columns': OrderedDict(),
        'filters': [],
        'notification': '',
    }

    principals = effective_principals(request)
    es = request.registry[ELASTIC_SEARCH]
    search_audit = request.has_permission('search_audit')

    # handling limit
    size = request.params.get('limit', 25)
    if size in ('all', ''):
        size = 99999
    else:
        try:
            size = int(size)
        except ValueError:
            size = 25

    search_term = request.params.get('searchTerm', '*')
    if search_term != '*':
        search_term = sanitize_search_string(search_term.strip())

    # Handling whitespaces in the search term
    if not search_term:
        result['notification'] = 'Please enter search term'
        return result

    if search_type is None:
        doc_types = request.params.getall('type')
        if '*' in doc_types:
            doc_types = []

        # handling invalid item types
        bad_types = [t for t in doc_types if t not in root.by_item_type]
        if bad_types:
            result['notification'] = "Invalid type: %s" ', '.join(bad_types)
            return result
    else:
        doc_types = [search_type]

    # Building query for filters
    if not doc_types:
        if request.params.get('mode') == 'picker':
            doc_types = []
        else:
            doc_types = ['antibody_lot', 'biosample', 'experiment', 'target',
                         'dataset', 'page', 'publication', 'software']
    else:
        for item_type in doc_types:
            qs = urlencode([
                (k.encode('utf-8'), v.encode('utf-8'))
                for k, v in request.params.items() if k != 'type' and v != item_type
            ])
            result['filters'].append({
                'field': 'type',
                'term': item_type,
                'remove': '{}?{}'.format(request.path, qs)
                })

    frame = request.params.get('frame')
    fields_requested = request.params.getall('field')
    if fields_requested:
        fields = {'embedded.@id', 'embedded.@type'}
        fields.update('embedded.' + field for field in fields_requested)
    elif frame in ['embedded', 'object']:
        fields = [frame + '.*']
    else:
        frame = 'columns'
        fields = set()
        if search_audit:
            fields.add('audit.*')
        for doc_type in (doc_types or root.by_item_type.keys()):
            collection = root[doc_type]
            if 'columns' not in (collection.type_info.schema or ()):
                fields.add('object.*')
            else:
                columns = collection.type_info.schema['columns']
                fields.update(
                    ('embedded.@id', 'embedded.@type'),
                    ('embedded.' + column for column in columns),
                )
                result['columns'].update(columns)

    # Builds filtered query which supports multiple facet selection
    query = get_filtered_query(search_term, sorted(fields), principals)

    if not result['columns']:
        del result['columns']

    # Sorting the files when search term is not specified
    if search_term == '*':
        query['sort'] = {
            'embedded.date_created': {
                'order': 'desc',
                'ignore_unmapped': True,
            },
            'embedded.label': {
                'order': 'asc',
                'missing': '_last',
                'ignore_unmapped': True,
            },
        }
        # Adding match_all for wildcard search for performance
        query['query']['match_all'] = {}
        del query['query']['query_string']

    # Setting filters
    query_filters = query['filter']['and']['filters']

    peak_files_uuids = []
    if 'regionid' in request.params:
        peak_files_uuids, notification = search_peaks(request)
        if not len(peak_files_uuids):
            if notification is 'success':
                result['notification'] = 'No results found for region entered'
            else:
                result['notification'] = 'Invalid region search term. \
                Please enter(GeneId, RSID or chr#-start-stop)'
            return result
        else:
            query_filters.append({
                'terms': {
                    'embedded.files.uuid': peak_files_uuids
                }
            })

    used_filters = {}
    for field, term in request.params.items():
        if field in ['type', 'limit', 'mode', 'searchTerm',
                     'format', 'frame', 'datastore', 'field']:
            continue

        # Add filter to result
        qs = urlencode([
            (k.encode('utf-8'), v.encode('utf-8'))
            for k, v in request.params.items() if v != term
        ])
        result['filters'].append({
            'field': field,
            'term': term,
            'remove': '{}?{}'.format(request.path, qs)
        })

        # Add filter to query
        if field.startswith('audit'):
            query_field = field
        else:
            query_field = 'embedded.' + field

        if query_field not in used_filters:
            query_terms = used_filters[query_field] = []
            query_filters.append({
                'terms': {
                    query_field: query_terms,
                }
            })
        used_filters[query_field].append(term)

    # Adding facets to the query
    # TODO: Have to simplify this piece of code
    facets = [
        ('type', {'title': 'Data Type'}),
    ]
    if len(doc_types) == 1 and 'facets' in types[doc_types[0]].schema:
        facets.extend(types[doc_types[0]].schema['facets'].items())

    if search_audit:
        for audit_facet in audit_facets:
            facets.append(audit_facet)

    for field, _ in facets:
        if field == 'type':
            query_field = '_type'
        elif field.startswith('audit'):
            query_field = field
        else:
            query_field = 'embedded.' + field
        agg_name = field.replace('.', '-')

        terms = [
            {'terms': {q_field: q_terms}}
            for q_field, q_terms in used_filters.items()
            if q_field != query_field
        ]
        terms.append(
            {'terms': {'principals_allowed.view': principals}}
        )

        query['aggs'][agg_name] = {
            'aggs': {
                agg_name: {
                    'terms': {
                        'field': query_field,
                        'min_doc_count': 0,
                        'size': 100
                    }
                }
            },
            'filter': {
                'bool': {
                    'must': terms,
                },
            },
        }

        # Handling region search using filters
        if len(peak_files_uuids):
            o_terms = query['aggs'][agg_name]['filter']
            n_terms = {'terms': {
                'embedded.files.uuid': peak_files_uuids
            }}
            query['aggs'][agg_name]['filter'] = {
                'bool': {
                    'must': [o_terms, n_terms]
                }
            }

        for count, used_facet in enumerate(result['filters']):
            if used_facet['field'] == 'searchTerm':
                continue
            if field != used_facet['field'] and used_facet['field'] != 'type':
                if used_facet['field'] != 'audit.category':
                    q_field = 'embedded.' + used_facet['field']
                else:
                    q_field = used_facet['field']
                if 'terms' in query['aggs'][agg_name]['filter']:
                    old_terms = query['aggs'][agg_name]['filter']
                    new_terms = {'terms': {
                        q_field: [used_facet['term']]
                    }}
                    query['aggs'][agg_name]['filter'] = {
                        'bool': {
                            'must': [old_terms, new_terms]
                        }
                    }
                else:
                    terms = query['aggs'][agg_name]['filter']['bool']['must']
                    flag = 0
                    for count, term in enumerate(terms):
                        if q_field in term['terms'].keys():
                            terms[count]['terms'][q_field].append(used_facet['term'])
                            flag = 1
                    if not flag:
                        terms.append({
                            'terms': {
                                q_field: [used_facet['term']]
                            }
                        })

    # Execute the query
    results = es.search(body=query, index='encoded',
                        doc_type=doc_types or None, size=size)

    # Loading facets in to the results
    if 'aggregations' in results:
        facet_results = results['aggregations']
        for field, facet in facets:
            agg_name = field.replace('.', '-')
            if agg_name not in facet_results:
                continue
            terms = facet_results[agg_name][agg_name]['buckets']
            if len(terms) < 2:
                continue
            result['facets'].append({
                'field': field,
                'title': facet['title'],
                'terms': terms,
                'total': facet_results[agg_name]['doc_count']
            })

    if doc_types == ['experiment'] and any(
            facet['doc_count'] > 0
            for facet in results['aggregations']['assembly']['assembly']['buckets']):
        search_params = request.query_string.replace('&', ',,')
        hub = request.route_url('batch_hub', search_params=search_params, txt='hub.txt')
        result['batch_hub'] = hgConnect + hub

    if doc_types == ['experiment']:
        result['batch_download'] = request.route_url('batch_download', search_params=request.query_string)

    # Loading result rows
    hits = results['hits']['hits']
    if frame in ['embedded', 'object'] and not len(fields_requested):
        result['@graph'] = [hit['_source'][frame] for hit in hits]
    elif fields_requested:
        result['@graph'] = [hit['_source']['embedded'] for hit in hits]
    else:  # columns
        for hit in hits:
            item_type = hit['_type']
            if 'columns' in types[item_type].schema:
                item = hit['_source']['embedded']
            else:
                item = hit['_source']['object']
            if 'audit' in hit['_source']:
                item['audit'] = hit['_source']['audit']
            result['@graph'].append(item)

    # Adding total
    result['total'] = results['hits']['total']
    result['notification'] = 'Success' if result['total'] else 'No results found'

    return result


@view_config(route_name='suggest', request_method='GET', permission='search')
def suggest(context, request, search_type=None):
    '''text = ''
    result = {
        '@id': '/suggest/' + ('?q=' + text),
        '@type': ['suggest'],
        'title': 'Suggest',
        '@graph': [],
    }
    if 'q' in request.params:
        text = request.params.get('q', '')
    else:
        return []
    es = request.registry[ELASTIC_SEARCH]
    query = {
        "suggester": {
            "text": text,
            "completion": {
                "field": "name_suggest",
                "size": 10
            }
        }
    }
    results = es.suggest(index='annotations', body=query)
    result['@id'] = '/suggest/' + ('?q=' + text)
    result['@graph'] = results['suggester'][0]['options']'''
    result = {
        "title": "Suggest",
        "@graph": [
            {
                "text": "BRCA1",
                "payload": {
                    "id": 2386
                },
                "score": 1
            },
            {
                "text": "BRCA1 associated RING domain 1",
                "payload": {
                    "id": 2033
                },
                "score": 1
            },
            {
                "text": "BRCA1 associated protein",
                "payload": {
                    "id": 2384
                },
                "score": 1
            },
            {
                "text": "BRCA1 associated protein-1 (ubiquitin carboxy-terminal hydrolase)",
                "payload": {
                    "id": 2032
                },
                "score": 1
            },
            {
                "text": "BRCA1-associated ATM activator 1",
                "payload": {
                    "id": 2385
                },
                "score": 1
            },
            {
                "text": "BRCA1/BRCA2-containing complex, subunit 3",
                "payload": {
                    "id": 2390
                },
                "score": 1
            },
            {
                "text": "BRCA1/BRCA2-containing complex, subunit 3 pseudogene 1",
                "payload": {
                    "id": 2391
                },
                "score": 1
            },
            {
                "text": "BRCA2",
                "payload": {
                    "id": 2388
                },
                "score": 1
            },
            {
                "text": "BRCA2 and CDKN1A interacting protein",
                "payload": {
                    "id": 2082
                },
                "score": 1
            },
            {
                "text": "BRCAA1",
                "payload": {
                    "id": 1395
                },
                "score": 1
            }
        ],
        "@type": [
            "suggest"
        ],
        "@id": "/suggest/?q=brca"
    }
    return result
