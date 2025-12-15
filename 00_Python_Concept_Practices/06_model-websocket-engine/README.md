# model-websocket-engine
POC of a model solving engine communicating with a frontend using websockets

#### Running the server with local access
1. Activate a new virtual envirionment with pipenv
2. Install dependencies with `pipenv sync`
3. Start the engine server with `inv eng` (runs on port 8765 by default)
4. Start the UI server with `inv ui` (runs on port 8000 by default)
5. Open the UI by navigating to http://localhost:8000


#### Running the server with external access
Follow the steps outlined above, but prior to step 4 you must edit `user_interface/index.html`. The websocket URL is hardcoded to "ws://127.0.0.1:8765". You must change this to the IP address or DNS name of the server running the websocket engine.
