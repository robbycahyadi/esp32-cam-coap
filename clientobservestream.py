import asyncio
import cv2
import numpy as np
from aiocoap import *

# Constants
SERVER_URI = "coap://192.168.110.28/stream"  # Replace with your CoAP server's IP
BUFFER_SIZE = 5  # Number of frames to buffer
WINDOW_NAME = "CoAP Video Stream"

async def observe_stream():
    """Observe the CoAP /stream resource and display video frames."""
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri=SERVER_URI, observe=0)  # Observe = 0 for subscription

    # Circular buffer to smooth video playback
    frame_buffer = []

    try:
        print(f"Subscribing to {SERVER_URI} for video stream...")
        async for response in protocol.request(request).observation:
            # Decode JPEG frame from the CoAP payload
            np_arr = np.frombuffer(response.payload, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is not None:
                # Add frame to the buffer
                frame_buffer.append(frame)
                if len(frame_buffer) > BUFFER_SIZE:
                    frame_buffer.pop(0)  # Keep the buffer size consistent

                # Display the frame from the buffer
                cv2.imshow(WINDOW_NAME, frame_buffer[0])

                # Exit when the user presses 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Exiting video stream.")
                    break
            else:
                print("Failed to decode a frame.")

    except Exception as e:
        print(f"Error during CoAP Observe: {e}")
    finally:
        cv2.destroyAllWindows()
        print("Stream closed.")

if __name__ == "__main__":
    asyncio.run(observe_stream())
