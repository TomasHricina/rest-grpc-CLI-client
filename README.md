# rest-grpc-CLI-client
CLI application which retrieves and prints data from either REST or gRPC server

Dependencies:
pytest
pytest-httpserver     # for testing REST HTTP client
flask                 # bonus: for testing on real server

Example local usage:

Test UUID = 123456

Start servers:  
python3 rest_server.py   # exists on port 4444  
python3 grpc_server.py   # exists on port 50051  
  
Use CLI client:  
Rest:  
python3 main.py --backend rest stat 123456 --base-url localhost:4444  
python3 main.py --backend rest stat 123456 --base-url localhost:4444 --output file.txt  
  
grpc:  
python3 main.py --backend grpc stat 123456  
python3 main.py --backend grpc read 123456 --chunk 7  # stream chunk_size = 7  
  
Testing:  
  
For REST, the test can be run in isolation with:  
pytest test_rest.client.py  
  
For gRPC:  

python3 grpc-server.py  
pytest test-grpc-client.py  
  
Current test requires grpc-server.py to be running.  
Therefore, it is more "integration" test, than unit test.  
Unit test should be able to run in isolation.  
  
Bonus:  
Test gRPC server with fake client:  
pytest test_grpc_server.py  
  
  
----Things to improve----  
Isolate gRPC client test, probably via mocking the gRPC server.  
Less flat file structure  
