from contentbase import (
    ROOT,
    upgrade_step,
)


@upgrade_step('analysis_step_run', '1', '2')
def analysis_step_run_1_2(value, system):
    # http://redmine.encodedcc.org/issues/3074
    root = system['registry'][ROOT]
    analysis_step_uuid = value.pop('analysis_step')
    analysis_step = root[analysis_step_uuid]
    analysis_step_version = root['versionof:{name}'.format(**analysis_step.properties)]
    value['analysis_step_version'] = str(analysis_step_version.uuid)
