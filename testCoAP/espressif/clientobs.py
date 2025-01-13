import asyncio
from aiocoap import *

async def coap_observable_request():
    # Define the CoAP server URI
    uri = "coap://192.168.110.28/Espressif"
    
    # Create a context for the CoAP client
    protocol = await Context.create_client_context()
    
    # Create a GET request message with Observe option
    request = Message(code=GET, uri=uri, observe=0)  # Observe=0 starts the observation
    
    try:
        # Send the request and handle the asynchronous responses
        requester = protocol.request(request)
        async for response in requester.observation:
            print(f"Response Code: {response.code}")
            print(f"Payload: {response.payload.decode('utf-8')}")
    except Exception as e:
        print(f"Failed to observe resource: {e}")

if __name__ == "__main__":
    asyncio.run(coap_observable_request())
