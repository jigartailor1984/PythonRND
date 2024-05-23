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
        self.breeze.ws_connect()
        connectResponse=breeze_pb2.ConnectResponse()
        connectResponse.message="Connection successful."

        return connectResponse

    
    def GetCustomerDetails(self, request, context):        
        response=self.breeze.get_customer_details(api_session=request.ApiSession)
        apiResponse=breeze_pb2.ApiResponse()
        apiResponse.Success=json.dumps(response['Success'])
        apiResponse.Status=response['Status']
        apiResponse.Error=json.dumps(response['Error'])

        return apiResponse
    
    def GetDematHolding(self, request, context):
        response=self.breeze.get_demat_holdings()
        apiResponse=breeze_pb2.ApiResponse()
        apiResponse.Success=json.dumps(response['Success'])
        apiResponse.Status=response['Status']
        apiResponse.Error=json.dumps(response['Error'])

        return apiResponse
    
    def GetLiveStreamingData(self, request, context):
        ticksQueue=[]
        def on_ticks(ticks):
            ticksQueue.append(json.dumps(ticks))
            
        self.breeze.on_ticks=on_ticks
        while context.is_active():
            while len(ticksQueue)>0:
                yield breeze_pb2.LiveStreamData(Data=ticksQueue.pop(0))
        
        self.breeze.on_ticks=None
    
    def SubscribeOrderNotification(self, request, context):
        response=self.breeze.subscribe_feeds(get_order_notification=True)
        subscribeResponse=breeze_pb2.SubscribeResponse()
        subscribeResponse.message=response['message']
        
        return subscribeResponse
    
    def UnsubscribeOrderNotification(self, request, context):
        response=self.breeze.unsubscribe_feeds(get_order_notification=True)
        print(response)
        unsubscribeResponse=breeze_pb2.UnsubscribeResponse()
        unsubscribeResponse.message=response['message']
        
        return unsubscribeResponse
        
        
    def GetNames(self, request, context):
        response=self.breeze.get_names(exchange_code=request.ExchangeCode, stock_code=request.StockCode)
        GetnamesResponse=breeze_pb2.GetNamesResponse()
        GetnamesResponse.ExchangeCode=response['exchange_code']
        GetnamesResponse.ExchangeStockCode=response['exchange_stock_code']
        GetnamesResponse.ISecStockCode=response['isec_stock_code']
        GetnamesResponse.ISecToken=response['isec_token']
        GetnamesResponse.CompanyName=response['company name']
        GetnamesResponse.ISecTokenLevel1=response['isec_token_level1']
        GetnamesResponse.ISecTokenLevel2=response['isec_token_level2']
        
        return GetnamesResponse
    
def serve():
    server=grpc.server(futures.ThreadPoolExecutor(10))
    breeze_pb2_grpc.add_BreezeApiServicer_to_server(BreezeApiServicer(),server)
    server.add_insecure_port("localhost:50053")
    server.start()
    server.wait_for_termination()

if __name__ =="__main__":
    serve()
