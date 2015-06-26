import pytest


@pytest.fixture
def biosample_0(submitter, lab, award, source, organism):
    return {
        'award': award['uuid'],
        'biosample_term_id': 'UBERON:349829',
        'biosample_type': 'tissue',
        'lab': lab['uuid'],
        'organism': organism['uuid'],
        'source': source['uuid'],
    }


@pytest.fixture
def biosample_1(biosample_0):
    item = biosample_0.copy()
    item.update({
        'schema_version': '1',
        'starting_amount': '1000',
    })
    return item


@pytest.fixture
def biosample_2(biosample_0):
    item = biosample_0.copy()
    item.update({
        'schema_version': '2',
        'subcellular_fraction': 'nucleus',
    })
    return item


@pytest.fixture
def biosample_3(biosample_0, biosample):
    item = biosample_0.copy()
    item.update({
        'schema_version': '3',
        'derived_from': [biosample['uuid']],
        'part_of': [biosample['uuid']],
        'encode2_dbxrefs': ['Liver'],
    })
    return item


@pytest.fixture
def biosample_4(biosample_0, encode2_award):
    item = biosample_0.copy()
    item.update({
        'schema_version': '4',
        'status': 'CURRENT',
        'award': encode2_award['uuid'],
    })
    return item


@pytest.fixture
def biosample_6(biosample_0):
    item = biosample_0.copy()
    item.update({
        'schema_version': '5',
        'sex': 'male',
        'age': '2',
        'age_units': 'week',
        'health_status': 'Normal',
        'life_stage': 'newborn',

    })
    return item


@pytest.fixture
def biosample_7(biosample_0):
    item = biosample_0.copy()
    item.update({
        'schema_version': '7',
        'worm_life_stage': 'embryonic',
    })
    return item


@pytest.fixture
def biosample_8(biosample_0):
    item = biosample_0.copy()
    item.update({
        'schema_version': '8',
        'model_organism_age': '15.0',
        'model_organism_age_units': 'day',
    })
    return item


@pytest.fixture
def biosample_9(root, biosample, publication):
    item = root.get_by_uuid(biosample['uuid'])
    properties = item.properties.copy()
    properties.update({
        'schema_version': '9',
        'references': [publication['identifiers'][0]],
    })
    return properties


@pytest.fixture
def biosample_10(root, biosample):
    item = root.get_by_uuid(biosample['uuid'])
    properties = item.properties.copy()
    properties.update({
        'schema_version': '10',
        'worm_synchronization_stage': 'starved L1 larva'
    })
    return properties


def test_biosample_upgrade(migrator, biosample_1):
    value = migrator.upgrade('biosample', biosample_1, target_version='2')
    assert value['schema_version'] == '2'
    assert value['starting_amount'] == 1000


def test_biosample_upgrade_unknown(migrator, biosample_1):
    biosample_1['starting_amount'] = 'Unknown'
    value = migrator.upgrade('biosample', biosample_1, target_version='2')
    assert value['schema_version'] == '2'
    assert 'starting_amount' not in value


def test_biosample_upgrade_empty_string(migrator, biosample_1):
    biosample_1['starting_amount'] = ''
    value = migrator.upgrade('biosample', biosample_1, target_version='2')
    assert value['schema_version'] == '2'
    assert 'starting_amount' not in value


def test_biosample_upgrade_exponent(migrator, biosample_1):
    biosample_1['starting_amount'] = '1 X 10^5'
    value = migrator.upgrade('biosample', biosample_1, target_version='2')
    assert value['schema_version'] == '2'
    assert value['starting_amount'] == 1e5


def test_biosample_upgrade_number(migrator, biosample_1):
    biosample_1['starting_amount'] = -1
    value = migrator.upgrade('biosample', biosample_1, target_version='2')
    assert value['schema_version'] == '2'
    assert value['starting_amount'] == -1


def test_biosample_upgrade_subcellular_fraction(migrator, biosample_2):
    value = migrator.upgrade('biosample', biosample_2, target_version='3')
    assert value['schema_version'] == '3'
    assert value['subcellular_fraction_term_name'] == 'nucleus'
    assert value['subcellular_fraction_term_id'] == 'GO:0005634'
    assert 'subcellular_fraction' not in value


def test_biosample_upgrade_subcellular_fraction_membrane(migrator, biosample_2):
    biosample_2['subcellular_fraction'] = 'membrane fraction'
    value = migrator.upgrade('biosample', biosample_2, target_version='3')
    assert value['schema_version'] == '3'
    assert value['subcellular_fraction_term_name'] == 'membrane'
    assert value['subcellular_fraction_term_id'] == 'GO:0016020'
    assert 'subcellular_fraction' not in value


def test_biosample_upgrade_array_to_string(migrator, biosample_3, biosample):
    value = migrator.upgrade('biosample', biosample_3, target_version='4')
    assert value['schema_version'] == '4'
    assert value['part_of'] == biosample['uuid']
    assert value['derived_from'] == biosample['uuid']


def test_biosample_upgrade_empty_array(migrator, biosample_3, biosample):
    biosample_3['derived_from'] = []
    biosample_3['part_of'] = []
    value = migrator.upgrade('biosample', biosample_3, target_version='4')
    assert value['schema_version'] == '4'
    assert 'part_of' not in value
    assert 'derived_from' not in value


def test_biosample_upgrade_encode2_dbxref(migrator, biosample_3):
    value = migrator.upgrade('biosample', biosample_3, target_version='4')
    assert value['schema_version'] == '4'
    assert value['dbxrefs'] == ['UCSC-ENCODE-cv:Liver']
    assert 'encode2_dbxrefs' not in value


def test_biosample_upgrade_encode2_complex_dbxref(migrator, biosample_3):
    biosample_3['encode2_dbxrefs'] = ['B-cells CD20+ (RO01778)']
    value = migrator.upgrade('biosample', biosample_3, target_version='4')
    assert value['schema_version'] == '4'
    assert value['dbxrefs'] == ['UCSC-ENCODE-cv:B-cells CD20+ (RO01778)']
    assert 'encode2_dbxrefs' not in value


def test_biosample_upgrade_status_encode2(migrator, biosample_4):
    value = migrator.upgrade('biosample', biosample_4, target_version='5')
    assert value['schema_version'] == '5'
    assert value['status'] == 'released'


def test_biosample_upgrade_status_encode3(migrator, biosample_4):
    biosample_4['award'] = 'ea1f650d-43d3-41f0-a96a-f8a2463d332f'
    value = migrator.upgrade('biosample', biosample_4, target_version='5')
    assert value['schema_version'] == '5'
    assert value['status'] == 'in progress'


def test_biosample_upgrade_model_organism(migrator, biosample_6):
    value = migrator.upgrade('biosample', biosample_6, target_version='7')
    assert value['schema_version'] == '7'
    assert 'sex' not in value
    assert 'age' not in value
    assert 'age_units' not in value
    assert 'health_status' not in value
    assert 'life_stage' not in value


def test_biosample_upgrade_model_organism_mouse(migrator, biosample_6):
    biosample_6['organism'] = '3413218c-3d86-498b-a0a2-9a406638e786'
    value = migrator.upgrade('biosample', biosample_6, target_version='7')
    assert value['schema_version'] == '7'
    assert 'sex' not in value
    assert value['model_organism_sex'] == 'male'
    assert 'age' not in value
    assert value['model_organism_age'] == '2'
    assert 'age_units' not in value
    assert value['model_organism_age_units'] == 'week'
    assert 'health_status' not in value
    assert value['model_organism_health_status'] == 'Normal'
    assert 'life_stage' not in value
    assert value['mouse_life_stage'] == 'postnatal'


def test_biosample_upgrade_inline(testapp, biosample_1):
    from contentbase.schema_utils import load_schema
    schema = load_schema('encoded:schemas/biosample.json')
    res = testapp.post_json('/biosample?validate=false&render=uuid', biosample_1)
    location = res.location

    # The properties are stored un-upgraded.
    res = testapp.get(location + '?frame=raw&upgrade=false').maybe_follow()
    assert res.json['schema_version'] == '1'

    # When the item is fetched, it is upgraded automatically.
    res = testapp.get(location).maybe_follow()
    assert res.json['schema_version'] == schema['properties']['schema_version']['default']

    res = testapp.patch_json(location, {})

    # The stored properties are now upgraded.
    res = testapp.get(location + '?frame=raw&upgrade=false').maybe_follow()
    assert res.json['schema_version'] == schema['properties']['schema_version']['default']


def test_biosample_upgrade_inline_unknown(testapp, biosample_1):
    from contentbase.schema_utils import load_schema
    schema = load_schema('encoded:schemas/biosample.json')
    biosample_1['starting_amount'] = 'Unknown'
    res = testapp.post_json('/biosample?validate=false&render=uuid', biosample_1)
    location = res.location
    res = testapp.patch_json(location, {})
    res = testapp.get(location + '?frame=raw&upgrade=false').maybe_follow()
    assert res.json['schema_version'] == schema['properties']['schema_version']['default']
    assert 'starting_amount' not in res.json


def test_biosample_worm_life_stage(migrator, biosample_7):
    biosample_7['organism'] = '2732dfd9-4fe6-4fd2-9d88-61b7c58cbe20'
    value = migrator.upgrade('biosample', biosample_7, target_version='8')
    assert value['schema_version'] == '8'
    assert value['worm_life_stage'] == 'mixed stage (embryonic)'


def test_biosample_age_pattern(migrator, biosample_8):
    value = migrator.upgrade('biosample', biosample_8, target_version='9')
    assert value['schema_version'] == '9'
    assert value['model_organism_age'] == '15'


def test_biosample_age_pattern2(migrator, biosample_8):
    biosample_8['model_organism_age'] = '15.0-16.0'
    value = migrator.upgrade('biosample', biosample_8, target_version='9')
    assert value['schema_version'] == '9'
    assert value['model_organism_age'] == '15-16'


def test_biosample_references(root, migrator, biosample,  biosample_9, publication, threadlocals, dummy_request):
    context = root.get_by_uuid(biosample['uuid'])
    dummy_request.context = context
    value = migrator.upgrade('biosample', biosample_9, target_version='10', context=context)
    assert value['schema_version'] == '10'
    assert value['references'] == [publication['uuid']]


def test_biosample_worm_synch_stage(root, migrator, biosample, biosample_10, dummy_request):
    context = root.get_by_uuid(biosample['uuid'])
    dummy_request.context = context
    biosample_10['organism'] = '2732dfd9-4fe6-4fd2-9d88-61b7c58cbe20'
    value = migrator.upgrade('biosample', biosample_10, target_version='11', context=context)
    assert value['schema_version'] == '11'
    assert value['worm_synchronization_stage'] == 'L1 larva starved after bleaching'
