import asyncio
import cv2
import numpy as np
from aiocoap import Context, Message, GET
import logging

# Enable detailed logging for debugging
logging.basicConfig(level=logging.INFO)

async def observe_stream():
    """
    Observes the CoAP /stream resource and displays the received frames using OpenCV.
    """
    # Create a CoAP client context
    context = await Context.create_client_context()

    # Create a GET request with observe option
    request = Message(code=GET, uri="coap://192.168.110.28/stream", observe=0)

    try:
        print("Sending observe request to CoAP server...")
        protocol = context.request(request)

        # Start receiving notifications
        response = await protocol.response
        print("Initial response received. Observing stream...")

        # Handle notifications (observations)
        async for notification in protocol.observation:
            try:
                print("Frame received, processing...")
                frame_data = notification.payload
                # Decode JPEG data into an OpenCV image
                frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

                if frame is not None:
                    cv2.imshow("CoAP Video Stream", frame)

                    # Exit gracefully if the user presses 'q'
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("Exiting...")
                        break
                else:
                    print("Corrupt or incomplete frame received. Skipping.")

            except Exception as e:
                print(f"Error processing frame: {e}")
    except Exception as e:
        print(f"Error: {e}. Retrying...")
        await asyncio.sleep(2)

    finally:
        # Release OpenCV resources
        cv2.destroyAllWindows()


async def observe_with_retry():
    """
    Observes the CoAP /stream resource with retries in case of errors.
    """
    while True:
        try:
            await observe_stream()
        except Exception as e:
            print(f"Observation error: {e}. Retrying in 2 seconds...")
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(observe_with_retry())
