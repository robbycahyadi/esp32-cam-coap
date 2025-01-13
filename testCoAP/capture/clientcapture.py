import asyncio
from aiocoap import *
import os
from datetime import datetime

async def coap_get_request():
    # Define the CoAP server URI
    uri = "coap://192.168.110.28/capture"
    
    # Create a context for the CoAP client
    protocol = await Context.create_client_context()
    
    # Create a GET request message
    request = Message(code=GET, uri=uri)
    
    try:
        # Send the request and wait for the response
        response = await protocol.request(request).response
        print(f"Response Code: {response.code}")
        print(f"Payload: {response.payload}")
        
        # Ensure the 'photos' directory exists
        os.makedirs("photos", exist_ok=True)
        
        # Get the current timestamp in the format yyyy-mm-dd_hh-mm-ss
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Save the payload (image) to a file with the timestamp
        file_path = f"photos/{timestamp}.jpg"
        with open(file_path, "wb") as f:
            f.write(response.payload)
        
        print(f"Image saved as {file_path}")
    except Exception as e:
        print(f"Failed to fetch resource: {e}")

if __name__ == "__main__":
    asyncio.run(coap_get_request())
