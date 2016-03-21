import logging
#logging.basicConfig(level=logging.DEBUG)

import pytest
import vcr

import gocd_parser.stream_status
import gocd_parser.retriever.server

# reduce typing!
g = gocd_parser.retriever.server.Server('http://localhost:8153/go')
f = 'tests/fixtures/cassettes/TestStreamStatus/'
S = gocd_parser.stream_status.StreamStatus

class TestStreamStatus:
    @vcr.use_cassette(f+'failing_stream.yaml')
    def test_failing_stream(self):
        '''Ensure a failing stream gives us expected status.'''
        status = S(g, 'DeployProduction')
        assert status.pipeline.name == 'DeployProduction'
        assert status.label == '14'
        assert len(status.value_stream.graph) == 11
        assert len(status.value_stream.graph.edges()) == 11

        external = status.dump()
        assert external['base_name'] == 'DeployProduction'
        assert external['schema_version'] == '1.1.0'
        assert external['status'] == 'blocked'
        assert external['base_status']['status'] == 'passing'
        assert external['base_status']['paths'] == {'passing': u'pipelines/DeployProduction/14/Deploy/1', 'failing': []}
        assert external['base_status']['seconds'] is not None
        assert external['base_status']['my_group'] == 'Production'
        assert external['base_status']['passing_label'] == '14'
        assert external['base_status']['ancestor_groups'] == [u'Development']
        assert external['base_status']['human_time'] is not None
        assert external['blocking']['FunctionalTests']['status'] == 'failing'
        assert external['blocking']['FunctionalTests']['paths'] == {'passing': u'pipelines/FunctionalTests/6/Deploy/1', 'failing': [u'tab/build/detail/FunctionalTests/9/Deploy/1/deployApplications']}
        assert external['blocking']['FunctionalTests']['seconds'] is not None
        assert external['blocking']['FunctionalTests']['my_group'] == 'Development'
        assert external['blocking']['FunctionalTests']['passing_label'] == '6'
        assert external['blocking']['FunctionalTests']['ancestor_groups'] == [u'Development']
        assert external['blocking']['FunctionalTests']['human_time'] is not None
