from concurrent import futures
import time
import math
import logging
import grpc
import cli_grpc_pb2 as pb2
import cli_grpc_pb2_grpc as pb2_grpc

from helper_functions import read_database, find_entry


class FileServicer(pb2_grpc.FileServicer):
    def __init__(self):
        self.db = read_database()

    def stat(self, request, context):
        _reply_data = find_entry(self.db, request.uuid)
        if isinstance(_reply_data, grpc.StatusCode):
            return _reply_data
        _reply = {"data": _reply_data[0]}
        return pb2.StatReply(**_reply)

    def read(self, request, context):
        _reply_data = find_entry(self.db, request.uuid)
        if isinstance(_reply_data, grpc.StatusCode):
            return _reply_data
        _chunk_size = request.size
        _data = _reply_data[1]['data']
        if _chunk_size == 0:
            _chunk_size = len(_data)
        _idx = 0
        while _idx < len(_data):
            _chunk = _data[_idx:_idx+_chunk_size]
            _idx += _chunk_size
            _reply_db_data = {"data": _chunk}
            _reply = {"data": _reply_db_data}
            yield pb2.ReadReply(**_reply)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_FileServicer_to_server(
        FileServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
