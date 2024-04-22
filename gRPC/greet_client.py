import greet_pb2
import greet_pb2_grpc
import time
import grpc

def get_client_stream_request():
    while True:
        name=input("Enter Name or nothing to stop chatting:")
        if name=="":
            break
        
        hello_request=greet_pb2.HelloRequest(greeting="Hello", name=name)
        yield hello_request
        time.sleep(1)

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub=greet_pb2_grpc.GreeterStub(channel)
        print("1. Say Hello - Unary")
        print("2. Parrot Say Hello - Server Streaming")
        print("3. Chatty Client Say Hello - Client Streaming")
        print("4. Interacting Hello - Bi-Directional streaming")
        rpc_call=input("Which rpc would you like to call: ")
        
        if rpc_call=="1":
            hello_request=greet_pb2.HelloRequest(greeting="Hello", name="Jigar")
            hello_reply=stub.SayHello(hello_request)
            print("say hello response received:")
            print(hello_reply)
        elif rpc_call=="2":
            hello_request=greet_pb2.HelloRequest(greeting="Hello", name="Jigar")
            hello_replies=stub.ParrotSaysHello(hello_request)
            for hello_reply in hello_replies:
                print("Parrot says hello response received:")
                print(hello_reply)
                
        elif rpc_call=="3":
            delayed_reply= stub.ChattyClientSaysHello(get_client_stream_request())
            print("ChattyClientSayHello Response received:")
            print(delayed_reply)
        elif rpc_call=="4":
            responses=stub.InteractingHello(get_client_stream_request())
            for response in responses:
                print("IntractingHello response recieved.")
                print(response)
            
            print("Say hello reply received:")

if __name__=="__main__":
    run()            
            
    