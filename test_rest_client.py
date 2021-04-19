import requests
import pytest
import uuid
from pytest_httpserver import HTTPServer
from rest_client import rest_api_client
from functools import partial


# URLs
test_uuid = str(uuid.uuid4())
relative_path = '/file/' + test_uuid
relative_read = relative_path + '/read/'
relative_stat = relative_path + '/stat/'



# backend test responses
test_json_correct = {
        "create_datetime": "2021-04-15",
        "size": "1024",
        "mimetype": "image/jpeg",
        "name": "cat.jpeg"
        }

test_json_bad_0 = {}
test_json_bad_1 = {
        "size": "1024",
        "mimetype": "image/jpeg",
        "name": "cat.jpeg"
        }
test_json_bad_2 = {
        "AAAAAA_datetime": "2021-04-15",
        "size": "1024",
        "mimetype": "image/jpeg",
        "name": "cat.jpeg"
        }

test_headers_correct = {'Content-Type': 'application/json', 'Content-Disposition': 'attachment; filename="cat.jpeg"'}
test_headers_bad_0 = {}
test_headers_bad_1 = {'Content-Type': 'application/json'}
test_headers_bad_2 = {'Content-Type': 'application/json', ' KONTENT-Disposition': 'attachment; filename="cat.jpeg"'}

#--------------------------------STAT-TESTS---------------------------------

@pytest.fixture(scope='function')
def setup_server_for_json(httpserver: HTTPServer):
    def _fixture(_json):
        httpserver.expect_request(relative_stat).respond_with_json(_json)
        
    return _fixture

def test_client_stat_correct(setup_server_for_json, httpserver: HTTPServer):
    partial_client = partial(rest_api_client, _uuid='', _subcommand='stat', port=None)
    setup_server_for_json(test_json_correct)
    api_client_result = partial_client(httpserver.url_for(relative_stat))
    assert set(api_client_result) == set(test_json_correct.keys())

def test_client_stat_bad_0(httpserver: HTTPServer):
    partial_client = partial(rest_api_client, _uuid='', _subcommand='stat', port=None)
    test_path = relative_stat
    test_json = test_json_bad_1
    httpserver.expect_request(test_path).respond_with_json(test_json)
    api_client_result = partial_client(httpserver.url_for(test_path))
    with pytest.raises(TypeError):
        assert set(api_client_result) == set(test_json_correct.keys())

@pytest.mark.parametrize("test_json", [test_json_bad_0, test_json_bad_1, test_json_bad_2])
def test_client_stat_param(setup_server_for_json, httpserver: HTTPServer, test_json):
    partial_client = partial(rest_api_client, _uuid='', _subcommand='stat', port=None)
    setup_server_for_json(test_json)
    api_client_result = partial_client(httpserver.url_for(relative_stat))
    with pytest.raises(TypeError):
        assert set(api_client_result) == set(test_json_correct.keys())


# #--------------------------------READ-TESTS---------------------------------

@pytest.fixture(scope='function')
def setup_server_for_header(httpserver: HTTPServer):
    def _fixture(_header):
        httpserver.expect_request(relative_read).respond_with_data(headers=_header)
    return _fixture

def test_client_read_correct(setup_server_for_header, httpserver: HTTPServer):
    partial_client = partial(rest_api_client, _uuid='', _subcommand='read', port=None)
    setup_server_for_header(test_headers_correct)
    api_client_result = partial_client(httpserver.url_for(relative_read))
    assert set(api_client_result) == set(test_headers_correct.keys())

@pytest.mark.parametrize("test_headers", [test_headers_bad_0, test_headers_bad_1, test_headers_bad_2])
def test_client_read_param(setup_server_for_header, httpserver: HTTPServer, test_headers):
    partial_client = partial(rest_api_client, _uuid='', _subcommand='read', port=None)
    setup_server_for_header(test_headers)
    api_client_result = partial_client(httpserver.url_for(relative_read))
    with pytest.raises(TypeError):
        assert set(api_client_result) == set(test_headers_correct.keys())




