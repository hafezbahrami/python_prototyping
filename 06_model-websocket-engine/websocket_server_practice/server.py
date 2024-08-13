"""
Basic WebSocket server that listens for incoming connections and echoes back any messages it receives:
- The echo function handles incoming connections. It listens for messages from the client and sends back 
        the same message prefixed with "Echo:".

- websockets.serve(echo, "localhost", 8765) starts the WebSocket server on localhost at port 8765.
"""
import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"Echo: {message}")

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server started on ws://localhost:8765")
asyncio.get_event_loop().run_forever()
