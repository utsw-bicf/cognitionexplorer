from snovault import (
    abstract_collection,
    calculated_property,
    collection,
    load_schema,
)
from pyramid.security import (
    Allow,
    Deny,
    Everyone,
)
from .base import (
    Item,
    paths_filtered_by_status,
)
from urllib.parse import quote_plus
from urllib.parse import urljoin
from .shared_calculated_properties import (
    CalculatedAssaySynonyms,
    CalculatedFileSetAssay,
    CalculatedFileSetBiosample,
    CalculatedSeriesAssay,
    CalculatedSeriesBiosample,
    CalculatedSeriesTreatment,
    CalculatedSeriesTarget,
    CalculatedVisualize
)

from itertools import chain
import datetime


def item_is_revoked(request, path):
    return request.embed(path, '@@object?skip_calculated=true').get('status') == 'revoked'



@abstract_collection(
    name='biodatasets',
    unique_key='accession',
    properties={
        'title': "Biodatasets",
        'description': 'Listing of all types of dataset.',
    })
class Biodataset(Item):
    base_types = ['Biodataset'] + Item.base_types
    embedded = [
        'files',
        'files.biospecimen',
        'files.award',
        #'files.bioreplicate',
        #'files.bioreplicate.bioexperiment',
        #'files.bioreplicate.bioexperiment.lab',
        'files.submitted_by',
        'files.lab',
        'revoked_files',
        #'revoked_files.bioreplicate',
        #'revoked_files.bioreplicate.bioexperiment',
        #'revoked_files.bioreplicate.bioexperiment.lab',
        'revoked_files.submitted_by',
        'submitted_by',
        'lab',
        'award',
        'award.pi.lab',
        'award.pi',
        'references'
    ]
    audit_inherit = [
        'original_files',
        'revoked_files',
        'contributing_files'
        'submitted_by',
        'lab',
        'award',
        'documents.lab',
    ]
    set_status_up = [
        'documents'
    ]
    set_status_down = []
    name_key = 'accession'
    rev = {
        'original_files': ('Biofile', 'biodataset'),
    }
    STATUS_ACL = {
        'released': [(Allow, 'group.verification', ['view_details'])]
    }
    
    @calculated_property(schema={
        "title": "Original files",
        "type": "array",
        "items": {
            "type": ['string', 'object'],
            "linkFrom": "Biofile.biodataset",
        },
        "notSubmittable": True,
    })
    def original_files(self, request, original_files):
        return paths_filtered_by_status(request, original_files)

    @calculated_property(schema={
        "title": "Contributing files",
        "type": "array",
        "items": {
            "type": "string",
            "linkTo": "Biofile",
        },
    })
    def contributing_files(self, request, original_files, status):
        derived_from = set()
        for path in original_files:
            properties = request.embed(path, '@@object?skip_calculated=true')
            derived_from.update(
                paths_filtered_by_status(request, properties.get('derived_from', []))
            )
        outside_files = list(derived_from.difference(original_files))
        if status in ('released'):
            return paths_filtered_by_status(
                request, outside_files,
                include=('released',),
            )
        else:
            return paths_filtered_by_status(
                request, outside_files,
                exclude=('revoked', 'deleted', 'replaced'),
            )

    @calculated_property(schema={
        "title": "Files",
        "type": "array",
        "items": {
            "type": "string",
            "linkTo": "Biofile",
        },
    })
    def files(self, request, original_files, status):
        if status in ('released', 'archived'):
            return paths_filtered_by_status(
                request, original_files,
                include=('released', 'archived'),
            )
        else:
            return paths_filtered_by_status(
                request, original_files,
                exclude=('revoked', 'deleted', 'replaced'),
            )

    @calculated_property(schema={
        "title": "Revoked files",
        "type": "array",
        "items": {
            "type": "string",
            "linkTo": "Biofile",
        },
    })
    def revoked_files(self, request, original_files):
        return [
            path for path in original_files
            if item_is_revoked(request, path)
        ]



    @calculated_property(condition='date_released', schema={
        "title": "Month released",
        "type": "string",
    })
    def month_released(self, date_released):
        return datetime.datetime.strptime(date_released, '%Y-%m-%d').strftime('%B, %Y')


class BiofileSet(Biodataset):
    item_type = 'biofile_set'
    base_types = ['BiofileSet'] + Biodataset.base_types
    schema = load_schema('encoded:schemas/biofile_set.json')
    embedded = Biodataset.embedded

    @calculated_property(schema={
        "title": "Contributing files",
        "type": "array",
        "items": {
            "type": "string",
            "linkTo": "Biofile",
        },
    })
    def contributing_files(self, request, original_files, related_files, status):
        files = set(original_files + related_files)
        derived_from = set()
        for path in files:
            properties = request.embed(path, '@@object?skip_calculated=true')
            derived_from.update(
                paths_filtered_by_status(request, properties.get('derived_from', []))
            )
        outside_files = list(derived_from.difference(files))
        if status in ('released'):
            return paths_filtered_by_status(
                request, outside_files,
                include=('released',),
            )
        else:
            return paths_filtered_by_status(
                request, outside_files,
                exclude=('revoked', 'deleted', 'replaced'),
            )

    @calculated_property(define=True, schema={
        "title": "Files",
        "type": "array",
        "items": {
            "type": "string",
            "linkTo": "Biofile",
        },
    })
    def files(self, request, original_files, related_files, status):
        if status in ('released'):
            return paths_filtered_by_status(
                request, chain(original_files, related_files),
                include=('released',),
            )
        else:
            return paths_filtered_by_status(
                request, chain(original_files, related_files),
                exclude=('revoked', 'deleted', 'replaced'),
            )

    @calculated_property(schema={
        "title": "Revoked files",
        "type": "array",
        "items": {
            "type": "string",
            "linkTo": "Biofile",
        },
    })
    def revoked_files(self, request, original_files, related_files):
        return [
            path for path in chain(original_files, related_files)
            if item_is_revoked(request, path)
        ]


"""
@collection(
    name='bioreferences',
    unique_key='accession',
    properties={
        'title': "Bioreference file set",
        'description': 'A set of reference files used by KCE.',
    })
class Bioreference(BiofileSet):
    item_type = 'bioreference'
    schema = load_schema('encoded:schemas/bioreference.json')
    embedded = BiofileSet.embedded + ['files.biodataset','award',
        'lab']


@collection(
    name='bioprojects',
    unique_key='accession',
    properties={
        'title': "Bioproject file set",
        'description': 'A set of files that comprise a project.',
    })
class Bioproject(BiofileSet, CalculatedFileSetAssay, CalculatedFileSetBiosample, CalculatedAssaySynonyms):
    item_type = 'bioproject'
    schema = load_schema('encoded:schemas/bioproject.json')
    embedded = BiofileSet.embedded + [
        'files.biodataset',
        'files.bioreplicate',
        'files.bioreplicate.bioexperiment',
        'award',
        'lab'
    ]
"""

@abstract_collection(
    name='bioseries',
    unique_key='accession',
    properties={
        'title': "Bioseries",
        'description': 'Listing of all types of series datasets.',
    })
class Bioseries(Biodataset, CalculatedSeriesAssay, CalculatedSeriesBiosample, CalculatedSeriesTarget, CalculatedSeriesTreatment, CalculatedAssaySynonyms):
    item_type = 'bioseries'
    base_types = ['Bioseries'] + Biodataset.base_types
    schema = load_schema('encoded:schemas/bioseries.json')
    embedded = Biodataset.embedded + [
        'references',
        'related_datasets.biospecimen',
        'related_datasets.files',
        'related_datasets.lab',
        'related_datasets.submitted_by',
        'related_datasets.award.pi.lab',
        'related_datasets.possible_controls',
        'related_datasets.possible_controls.lab',
        'related_datasets.references',
        'files.lab',
        'award',
        'lab'
    ]

    @calculated_property(schema={
        "title": "Revoked datasets",
        "type": "array",
        "items": {
            "type": "string",
            "linkTo": "Biofile",
        },
    })
    def revoked_datasets(self, request, related_datasets):
        return [
            path for path in related_datasets
            if item_is_revoked(request, path)
        ]


@collection(
    name='bioexperiment-series',
    unique_key='accession',
    properties={
        'title': "Bioexperiment series",
        'description': 'A series that groups two or more experiments.',
    })
class BioexperimentSeries(Bioseries):
    item_type = 'bioexperiment_series'
    schema = load_schema('encoded:schemas/bioexperiment_series.json')
    name_key = 'accession'
    embedded = [
        'contributing_awards',
        'contributors',
        'award',
        'lab',
        'related_datasets.lab',
        'related_datasets.award',
    ]

    @calculated_property(schema={
        "title": "Assay title",
        "type": "array",
        "items": {
            "type": "string",
        },
    })
    def assay_title(self, request, related_datasets):
        return request.select_distinct_values('assay_title', *related_datasets)

    @calculated_property(schema={
        "title": "Awards",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Award",
        },
    })
    def contributing_awards(self, request, related_datasets):
        return request.select_distinct_values('award', *related_datasets)

    @calculated_property(schema={
        "title": "Labs",
        "type": "array",
        "items": {
            "type": 'string',
            "linkTo": "Lab",
        },
    })
    def contributors(self, request, related_datasets):
        return request.select_distinct_values('lab', *related_datasets)
