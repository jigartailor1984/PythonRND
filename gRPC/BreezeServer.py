from breeze_connect import BreezeConnect
from concurrent import futures
import time
import json

import grpc
import breeze_pb2
import breeze_pb2_grpc


class BreezeApiServicer(breeze_pb2_grpc.BreezeApiServicer):
    breeze=None
    def Connect(self, request, context):
        self.breeze=BreezeConnect(request.AppKey)
        self.breeze.generate_session(api_secret=request.SecretKey, session_token=request.ApiSession)
        connectResponse=breeze_pb2.ConnectResponse()
        connectResponse.message="Connection successful."
        
        return connectResponse

    
    def GetCustomerDetails(self, request, context):        
        response=self.breeze.get_customer_details(api_session=request.ApiSession)
        apiResponse=breeze_pb2.ApiResponse()
        print(response)
        apiResponse.Success=json.dumps(response['Success'])
        apiResponse.Status=response['Status']
        apiResponse.Error=json.dumps(response['Error'])

        return apiResponse
        
def serve():
    server=grpc.server(futures.ThreadPoolExecutor(10))
    breeze_pb2_grpc.add_BreezeApiServicer_to_server(BreezeApiServicer(),server)
    server.add_insecure_port("localhost:50053")
    server.start()
    server.wait_for_termination()

if __name__ =="__main__":
    serve()
