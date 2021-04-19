import argparse
import sys
import grpc_client
import rest_client
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()  
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)

parser = argparse.ArgumentParser(description='Provide a command ``file-client`` with following usage::', formatter_class=SmartFormatter)
parser.add_argument(dest='subcommand', type=str, nargs=1, choices=('stat', 'read'), 
help="R|stat-Prints the file metadata in a human-readable manner\n"
"read-Outputs the file content (add --chunk, for chunk size, chunk=0 => everything at once")
parser.add_argument(dest='UUID', type=str, nargs=1, help='UUID')
parser.add_argument('--backend', default=['grpc'], nargs=1, choices=('grpc', 'rest'), help='Set a backend to be used, choices are grpc and rest. Default is grpc.')
parser.add_argument('--output', default=['-'])
parser.add_argument('--chunk', default=0)
group = parser.add_mutually_exclusive_group()
group.add_argument('--grpc-server', help='Set a host and port of the gRPC server. Default is localhost:50051.')
group.add_argument('--base-url', help='Set a base URL for a REST server. Default is http://localhost/.')
args = vars(parser.parse_args())
backend, subcommand, uuid = *args['backend'], *args['subcommand'], *args['UUID']
grcp_server, url_server, output = args['grpc_server'], args['base_url'], args['output']
chunk_size = args['chunk']

if output != ['-']:
    sys.stdout = open(output, 'w')

try:
    chunk_size = int(chunk_size)
except TypeError:
    print('Chunk size needs to be an integer')
    exit()

# set defaults
if backend == 'grpc':
    server = grcp_server
    if not server:
        server = 'localhost:50051'
        if url_server:
            print('WARNING: You inputted both grcp server and REST url - REST url will be ignored')

elif backend == 'rest':
    server = url_server
    if not server:
        server = 'http://localhost/'
        if grcp_server:
            print('WARNING: You inputted both grcp server and REST url - grpc server will be ignored')      

print()
print(now)
print('-------User-Input-------')
print('backend: ', backend)
print('server: ', server)
print('uuid: ', uuid)
print('subcommand: ', subcommand)
print()

print('-------API-Result-------')

if backend == 'grpc':
    if subcommand == 'stat':
        print(grpc_client.run(uuid, subcommand, server))
    elif subcommand == 'read':
        print(grpc_client.run(uuid, subcommand, server, chunk=chunk_size))
elif backend == 'rest':
    res = rest_client.rest_api_client(server, uuid, subcommand)
    if isinstance(res, dict):
        print(res)
    else:
        print(404)

if output != ['-']:
    sys.stdout.close()
