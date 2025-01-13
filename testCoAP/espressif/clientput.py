import asyncio
import random
from aiocoap import Context, Message, PUT

async def coap_put():
    # Define the target CoAP server
    uri = "coap://192.168.110.28/Espressif"  # Replace with actual IP and port
    
    # Create the CoAP context
    context = await Context.create_client_context()
    try:
        while True:
            # Generate a random humidity value between 1 and 100
            humidity = random.randint(1, 100)
            payload = f"Humidity: {humidity}"
            
            # Create the CoAP PUT request
            request = Message(code=PUT, uri=uri, payload=payload.encode('utf-8'))
            
            # Send the request and handle the response
            try:
                response = await context.request(request).response
                print(f"Response Code: {response.code}")
                print(f"Response Payload: {response.payload.decode('utf-8')}")
            except Exception as e:
                print(f"Request failed: {e}")
            
            # Wait for 1 second before the next iteration
            await asyncio.sleep(1)
    finally:
        await context.shutdown()

# Run the async function
if __name__ == "__main__":
    asyncio.run(coap_put())
