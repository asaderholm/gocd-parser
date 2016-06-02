import logging
logging.basicConfig(level=logging.DEBUG)

import pytest
import vcr

import gocd_parser.handler.compare
import gocd_parser.handler.compare.change as change
import gocd_parser.retriever.server

# reduce typing!
g = gocd_parser.retriever.server.Server('http://localhost:8153/go')
f = 'tests/fixtures/cassettes/TestCompare/'
C = gocd_parser.handler.compare.Compare

def assert_commits_and_pipelines(c):
    assert len(c.materials) == 10
    assert c.materials[0].name == 'https://github.com/greenmoss/gocd_source'
    assert c.materials[0].branch == 'master'
    assert c.materials[0].type == 'git'
    assert len(c.materials[0].changes) == 2
    assert c.materials[0].changes[0].revision == 'dd154416726d3e813145777baef747f411dc1fca'
    assert c.materials[0].changes[0].modifier_name == 'Kurt Yoder'
    assert c.materials[0].changes[0].modifier_email == 'ktygithub@yoderhome.com'
    assert c.materials[0].changes[0].modifier_time == 1458403792
    assert c.materials[0].changes[0].comment == 'Get diagnostic output from run.sh'

    assert c.materials[9].name == 'AppDevelopment'
    assert c.materials[9].type == 'pipeline'
    assert len(c.materials[9].changes) == 4
    assert c.materials[9].changes[0].revision == 'AppDevelopment/5/Package/1'
    assert c.materials[9].changes[0].revision_url == '/go/pipelines/AppDevelopment/5/Package/1'
    assert c.materials[9].changes[0].label == '5'
    assert c.materials[9].changes[0].label_url == '/go/pipelines/value_stream_map/AppDevelopment/5'
    assert c.materials[9].changes[0].completed == 1458404255

class TestCompare:
    @vcr.use_cassette(f+'commits_and_pipelines_v16_3.yaml')
    def test_commits_and_pipelines_v16_3(self):
        '''All expected git commits and pipelines appear in the list of changes.
        Test against 16.3'''
        c = C(g, 'DeployProduction', '12', '13')
        assert_commits_and_pipelines(c)

    @vcr.use_cassette(f+'commits_and_pipelines_v16_4.yaml')
    def test_commits_and_pipelines_v16_4(self):
        '''All expected git commits and pipelines appear in the list of changes.
        Test against 16.4'''
        g = gocd_parser.retriever.server.Server('http://localhost:8153/go', 'chester', 'badger')
        c = C(g, 'DeployProduction', '12', '13')
        assert_commits_and_pipelines(c)

    @vcr.use_cassette(f+'commits_and_pipelines_v16_5.yaml')
    def test_commits_and_pipelines_v16_5(self):
        '''All expected git commits and pipelines appear in the list of changes.
        Test against 16.5'''
        g = gocd_parser.retriever.server.Server('http://localhost:8153/go')
        c = C(g, 'DeployProduction', '12', '13')
        assert_commits_and_pipelines(c)

    @vcr.use_cassette(f+'unknown_material.yaml')
    def test_none_passing(self):
        '''Unrecognized material should raise an exception.'''
        with pytest.raises(gocd_parser.handler.compare.CompareException):
            c = C(g, 'DeployProduction', '12', '13')

    @vcr.use_cassette(f+'pipeline_non_alphanum.yaml')
    def test_pipeline_non_alphanum(self):
        '''Ensure pipeline non-alphanumeric characters are detected properly
        for setting the pipeline name. Note the problem is actually with
        <wbr/>, not with the non-alphanumeric characters.'''

        g = gocd_parser.retriever.server.Server('http://localhost:8153/go', 'chester', 'badger')
        c = C(g, 'DeployProduction', '14', '15')
        print c.materials
        assert c.materials[0].name == 'with-dashes.dots'

    def test_stripped_tags(self):
        '''Ensure weird tags are properly stripped from change info.'''
        assert change.convert_tags('Things') == 'Things'
        assert change.convert_tags('User Name &lt;uname@some.domain>') == 'User Name <uname@some.domain>'
        assert change.convert_tags('User Name <uname@some.domain&gt;') == 'User Name <uname@some.domain>'
