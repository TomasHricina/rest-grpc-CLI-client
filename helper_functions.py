from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
import grpc
import json


def string_to_timestamp_format(date, format='%Y-%m-%d'):
    timestamp = Timestamp()
    timestamp.FromDatetime(datetime.strptime(date, format))
    return timestamp


def seconds_to_timestamp(seconds):
    timestamp = Timestamp()
    timestamp.FromSeconds(seconds)
    return timestamp

def datetime_to_timestamp(datetime):
    timestamp = Timestamp()
    timestamp.FromDatetime(datetime)
    return timestamp


def read_database():
    with open('db.json') as json_file:
        data = json.load(json_file)
    return data

def find_entry(_db, _target_uuid):
    for entry in _db:
        if 'uuid' not in entry.keys():
            return grpc.StatusCode.FAILED_PRECONDITION
        if entry['uuid'] == _target_uuid.value:
            try:
                stat_dict = dict()
                stat_dict['create_datetime'] = string_to_timestamp_format(entry['create_datetime'])
                stat_dict['size'] = int(entry['size'])
                stat_dict['mimetype'] = entry['mimetype']
                stat_dict['name'] = entry['name']
                read_dict = dict()
                read_dict['data'] = bytes(entry['data'], 'utf-8')
            except (KeyError, ValueError):
                return grpc.StatusCode.FAILED_PRECONDITION
            else:
                return stat_dict, read_dict
    else:
        return grpc.StatusCode.NOT_FOUND
