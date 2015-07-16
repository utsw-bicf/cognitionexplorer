from contentbase import upgrade_step


@upgrade_step('pipeline', '', '2')
def pipeline_0_2(value, system):
    # http://redmine.encodedcc.org/issues/3001

    value['lab'] = "a558111b-4c50-4b2e-9de8-73fd8fd3a67d"  # /labs/encode-processing-pipeline/
    value['award'] = "b5736134-3326-448b-a91a-894aafb77876"  # /awards/ENCODE/


@upgrade_step('pipeline', '2', '3')
def pipeline_2_3(value, system):
    # http://redmine.encodedcc.org/issues/3093
    value.pop('name', None)
    value.pop('version', None)
    value.pop('end_points', None)
