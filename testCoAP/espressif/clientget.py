import asyncio
from aiocoap import *

async def coap_get_request():
    # Define the CoAP server URI
    uri = "coap://192.168.110.28/Espressif"
    
    # Create a context for the CoAP client
    protocol = await Context.create_client_context()
    
    # Create a GET request message
    request = Message(code=GET, uri=uri)
    
    try:
        # Send the request and wait for the response
        response = await protocol.request(request).response
        print(f"Response Code: {response.code}")
        print(f"Payload: {response.payload}")
    except Exception as e:
        print(f"Failed to fetch resource: {e}")

if __name__ == "__main__":
    asyncio.run(coap_get_request())
