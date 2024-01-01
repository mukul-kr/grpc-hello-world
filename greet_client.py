import greet_pb2_grpc
import greet_pb2
import time
import grpc

def get_client_stream_requests():
    while True:
        name = input("Please enter a name: (empty for ending response)")
        if name == "":
            break
        hello_request = greet_pb2.HelloRequest(greeting="Hello", name=name)
        yield hello_request
        time.sleep(1)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        print("1. SayHello - Unary")
        print("2. ParrotSaysHello - Server Side Streaming")
        print("3. ChattyClientSaysHello - Client Side Streaming")
        print("4. InteractingHello - Both Streaming")
        rpc_call = int(input("Which RPC call do you want to make? "))

        if rpc_call == 1:
            print("Calling SayHello RPC")
            hello_request = greet_pb2.HelloRequest(greeting="Hello", name="World")
            hello_reply = stub.SayHello(hello_request)
            print(f"Say Hello Response: {hello_reply}")
        elif rpc_call == 2:
            print("Calling SayHello RPC")
            hello_request = greet_pb2.HelloRequest(greeting="Hello", name="World")
            hello_replies = stub.ParrotSaysHello(hello_request)
            for hello_reply in hello_replies:
                print(f"ParrotSaysHello Response: {hello_reply}")
        elif rpc_call == 3:
            delayed_reply = stub.ChattyClientSaysHello(get_client_stream_requests())
            print("ChattyClientSaysHello Response: ")
            print(delayed_reply)
        elif rpc_call == 4:
            responses = stub.InteractingHello(get_client_stream_requests())
            for response in responses:
                print(f"InteractingHello Response: {response}")
                


if __name__ == '__main__':
    run()