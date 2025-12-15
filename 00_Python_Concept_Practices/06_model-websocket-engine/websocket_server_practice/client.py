"""
A simple WebSocket client that connects to the server, sends a message, and receives the echoed response:
- The hello function connects to the WebSocket server at ws://localhost:8765.
        It sends a message to the server and waits for the echoed response, then prints it.

        
Running the Example
- Start the Server: Run the server code (websocket_client.py) in one terminal or script. This will start the WebSocket server.

- Run the Client: Run the client code in another terminal or script. The client will connect to the server, send a message, and print the response.
"""

import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message = "Hello, WebSocket!"
        print(f"Sending message: {message}")
        await websocket.send(message)
        
        response = await websocket.recv()
        print(f"Received response: {response}")

asyncio.get_event_loop().run_until_complete(hello())
