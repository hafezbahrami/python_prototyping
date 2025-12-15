# 1 Server

A WebSocket server written in Python (server.py) that listens for incoming connections and echoes received messages. These messages could come from any other server, either written in another python files (such as client.py), or from an html file (such as index.html).

In our server:
- The echo function handles incoming connections. It listens for messages from the client and sends back the same message prefixed with "Echo:".
- websockets.serve(echo, "localhost", 8765) starts the WebSocket server on localhost at port 8765.

```python
async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(f"Echo: {message}")

start_server = websockets.serve(echo, "localhost", 8765)
```

# 2 CLient
Client is the one send some messeage to the server and recieves something else. In this example, we have 2 types of servers, as below.

### 2-1 Python client
In client.py:
- The hello function connects to the WebSocket server at ws://localhost:8765.
- It sends a message to the server and waits for the echoed response, then prints it.

```python
async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message = "Hello, WebSocket!"
        print(f"Sending message: {message}")
        await websocket.send(message)
        
        response = await websocket.recv()
        print(f"Received response: {response}")

asyncio.get_event_loop().run_until_complete(hello())
```


### 2-2 HTML CLient
This is usually when we want to create UI, and we want to connect to the server through the HTML file.



# 3 Run
Running the Example:
- **Start the Server**: Run the server code in one terminal or script. This will start the WebSocket server.
    - Now, our server is ready to listen to any incoming message.

- **Run the Client**: 
    - If client is client.py: Run the client code in another terminal or script. The client will connect to the server, send a message, and print the response.
    - If client is index.html: Open the html file in a browser. It automatically connects to the server we started above.



# Appendix: Explanation of the HTML File (`index.html`)

The `index.html` file provides a simple user interface (UI) for interacting with the WebSocket server. Below is a detailed explanation of its structure and functionality:

### A1 Basic Structure

The HTML file consists of a few key elements:

- **Title and Header**: 
  - `<title>WebSocket Client</title>`: Sets the title of the web page, which appears in the browser's tab.
  - `<h1>WebSocket Client</h1>`: Displays a large heading on the page with the text "WebSocket Client".

- **Input and Button**:
  - `<input type="text" id="messageInput" placeholder="Enter a message" />`: A text input field where users can type a message that they want to send to the WebSocket server.
  - `<button onclick="sendMessage()">Send Message</button>`: A button that, when clicked, triggers the `sendMessage()` JavaScript function to send the message typed in the input field to the server.

- **Output Div**:
  - `<div id="output"></div>`: An empty `div` element that serves as a container to display messages. Messages sent by the user and responses from the server are appended here.

### A2 JavaScript Functionality

The JavaScript code embedded in the `index.html` file is responsible for managing the WebSocket connection and handling UI updates:

- **Creating a WebSocket Connection**:
```javascript
  const socket = new WebSocket('ws://localhost:8765');
```
    - This line establishes a new WebSocket connection to the server running at ws://localhost:8765. The WebSocket object is used to interact with the server.

- **Handling Connection Open Event**:

```javascript
socket.onopen = function(event) {
    console.log("Connected to WebSocket server");
    document.getElementById('output').innerHTML += "<p>Connected to WebSocket server</p>";
};

```
    - The onopen event listener is triggered when the WebSocket connection is successfully established. It logs a confirmation message to the browser console and updates the output div on the web page to inform the user that the connection is active.

- **Receiving Messages from the Server**:
```javascript
socket.onmessage = function(event) {
    console.log("Received message from server:", event.data);
    document.getElementById('output').innerHTML += `<p>Server: ${event.data}</p>`;
};
```
    - The onmessage event listener is activated whenever the WebSocket server sends a message to the client. The received message (event.data) is logged to the console and displayed in the output div on the web page, prefixed with "Server:".
