from grpc_server import FileServicer
import cli_grpc_pb2 as pb2
from helper_functions import read_database, find_entry


top_uuid = '123456'
encoding = 'utf-8'
client_chunk_size = 3


def test_stat_with_real_server():
    service = FileServicer()
    db = read_database()
    uuid = pb2.Uuid(**{'value': top_uuid})

    req = pb2.StatRequest(**{"uuid": uuid})
    response = service.stat(req, None)

    try:
        response.data
    except (AttributeError, TypeError):
        raise FileNotFoundError

    db_lookup = find_entry(db, uuid)
    db_lookup = db_lookup[0]

    assert db_lookup['create_datetime'] == response.data.create_datetime
    assert db_lookup['size'] == response.data.size
    assert db_lookup['mimetype'] == response.data.mimetype
    assert db_lookup['name'] == response.data.name
    assert len(db_lookup) == 4


def test_read_with_real_server():

    service = FileServicer()
    db = read_database()
    client_chunk_size = 3

    uuid = pb2.Uuid(**{'value': top_uuid})
    req = pb2.ReadRequest(**{"uuid": uuid, "size": client_chunk_size})
    response = service.read(req, None)
    response_list = list(response)
    first_server_chunk_size = len(response_list[0].data.data)
    assert first_server_chunk_size != 0

    if client_chunk_size == 0:
        client_chunk_size = first_server_chunk_size
    else:
        for resp in response_list[:-1]:
            assert len(resp.data.data) == first_server_chunk_size 
    
    try:
        db_lookup = find_entry(db, uuid)
        db_lookup = db_lookup[1]
        db_lookup = db_lookup['data'].decode(encoding)
    except (AttributeError, TypeError):
        raise FileNotFoundError

    # match all the chunks with db
    for idx, chunk in enumerate(response_list):
        chunk_slice = slice(idx*client_chunk_size, idx*client_chunk_size+client_chunk_size)
        assert chunk.data.data.decode(encoding) == db_lookup[chunk_slice]
