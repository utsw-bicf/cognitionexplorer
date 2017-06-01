import pytest


@pytest.fixture
def base_reference_epigenome(testapp, lab, award):
    item = {
        'award': award['uuid'],
        'lab': lab['uuid'],
        'status': 'ready for review'
    }
    return testapp.post_json('/reference-epigenomes', item, status=201).json['@graph'][0]


@pytest.fixture
def base_experiment(testapp, lab, award):
    item = {
        'award': award['uuid'],
        'lab': lab['uuid'],
        'assay_term_name': 'RNA-seq',
        'status': 'ready for review'
    }
    return testapp.post_json('/experiment', item, status=201).json['@graph'][0]


@pytest.fixture
def hg19_file(testapp, base_reference_epigenome, award, lab):
    item = {
        'dataset': base_reference_epigenome['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'file_format': 'bigBed',
        'file_format_type': 'narrowPeak',
        'file_size': 345,
        'assembly': 'hg19',
        'md5sum': 'e002cd204df36d93dd070ef0712b8eed',
        'output_type': 'replicated peaks',
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def GRCh38_file(testapp, base_experiment, award, lab):
    item = {
        'dataset': base_experiment['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'file_format': 'bigBed',
        'file_format_type': 'narrowPeak',
        'file_size': 345,
        'assembly': 'GRCh38',
        'md5sum': 'e002cd204df36d93dd070ef0712b8ee7',
        'output_type': 'replicated peaks',
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


def test_assembly(testapp, base_reference_epigenome, base_experiment, hg19_file, GRCh38_file):
    res = testapp.get(base_reference_epigenome['@id']+'@@index-data')
    assert res.json['object']['assembly'] == ['hg19']
    testapp.patch_json(base_reference_epigenome['@id'], {'related_datasets': [base_experiment['@id']]})
    res = testapp.get(base_reference_epigenome['@id']+'@@index-data')
    assert 'GRCh38' in res.json['object']['assembly'] and 'hg19' in res.json['object']['assembly']
