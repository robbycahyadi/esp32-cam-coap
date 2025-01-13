import asyncio
import cv2
import numpy as np
from aiocoap import *

async def fetch_stream():
    uri = "coap://192.168.110.28/stream"  # Replace with your CoAP server's IP and endpoint
    protocol = await Context.create_client_context()

    try:
        print("Starting video stream...")
        while True:
            # Send GET request for the next frame
            request = Message(code=GET, uri=uri)
            response = await protocol.request(request).response

            # Decode the frame (assumes JPEG format)
            np_arr = np.frombuffer(response.payload, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is not None:
                cv2.imshow("CoAP Video Stream", frame)
            else:
                print("Failed to decode frame.")

            # Break if the user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting video stream.")
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(fetch_stream())
