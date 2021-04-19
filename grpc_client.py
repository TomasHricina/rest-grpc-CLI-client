from __future__ import print_function
import logging
import grpc
import cli_grpc_pb2 as pb2
import cli_grpc_pb2_grpc as pb2_grpc

default_netloc = 'localhost:50051'

def stat_client(stub, _uuid):
    uuid = pb2.Uuid(**{'value': _uuid})
    req = pb2.StatRequest(**{"uuid": uuid})
    try:
        stat_reply = stub.stat(req)
        return stat_reply
    except grpc.RpcError:
        return 404


def read_client(stub, _uuid, chunk_size=1):
    uuid = pb2.Uuid(**{'value': _uuid})
    req = pb2.ReadRequest(**{"uuid": uuid, "size": chunk_size})
    try:
        read_replies = stub.read(req)
        read_replies = list(read_replies)
    except grpc.RpcError:
        return 404
    else:
        if read_replies:
            return read_replies
        else:
            return 404
            
def run(_uuid, _subcommand, _netloc=default_netloc, chunk=1):
    with grpc.insecure_channel(_netloc) as channel:
        stub = pb2_grpc.FileStub(channel)
        if _subcommand == 'stat': 
            return stat_client(stub, _uuid)
        elif _subcommand == 'read':
            return read_client(stub, _uuid, chunk)
