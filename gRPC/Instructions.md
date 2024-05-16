# Instructions to setup and run service

1. Install tool grpc.io using following command
   ```bat
   pip install grpcio-tools
   ```
2. Generate grpc service file from proto file
   ```bat
   python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/greet.proto
   ```
