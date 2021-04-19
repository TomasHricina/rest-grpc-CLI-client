from grpc_server import serve
from grpc_client import stat_client, read_client
import cli_grpc_pb2 as pb2
import cli_grpc_pb2_grpc as pb2_grpc
from helper_functions import read_database, find_entry
import grpc
import pytest


# values for testing
top_uuid = '123456'
encoding = 'utf-8'
default_netloc = 'localhost:50051'
client_chunk_size = 3
mock_db_data = "12345678910"
mock_db_list = []
idx = 0
while idx < len(mock_db_data):
    chunk = mock_db_data[idx:idx+client_chunk_size]
    idx += client_chunk_size
    mock_db_list.append(chunk)

def test_client_stat_server():
    with grpc.insecure_channel(default_netloc) as channel:
        stub = pb2_grpc.FileStub(channel)
        response = stat_client(stub, top_uuid)
        uuid = pb2.Uuid(**{'value': top_uuid})
        db = read_database()
        db_lookup = find_entry(db, uuid)
        db_lookup = db_lookup[0]
        assert db_lookup['create_datetime'] == response.data.create_datetime
        assert db_lookup['size'] == response.data.size
        assert db_lookup['mimetype'] == response.data.mimetype
        assert db_lookup['name'] == response.data.name


def test_client_read_real_server():
    with grpc.insecure_channel(default_netloc) as channel:
        stub = pb2_grpc.FileStub(channel)
        response = read_client(stub, top_uuid, client_chunk_size)
        for _idx, _val in enumerate(response):
            assert _val.data.data.decode('utf-8') == mock_db_list[_idx]

