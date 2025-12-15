#!/usr/bin/env python

import struct
import asyncio

import websockets
from websockets import WebSocketServerProtocol

from engine import Model  # type: ignore


async def evaluation_engine(websocket: WebSocketServerProtocol):

    model = Model.build_example()
    print("Model Evaluation Engine\n2024Ryan Barden")
    print(model.to_pretty())

    await websocket.send(
        "Model Evaluation Engine\n2024 Ryan Barden\n\n" + model.to_pretty()
    )
    message_struct = struct.Struct("d")
    while True:
        # Wait for input
        raw_data: bytes = await websocket.recv()                                    # get the raw data from UI, in bytes
        unpacked_data = tuple(i[0] for i in message_struct.iter_unpack(raw_data))   # Unpack the rawa data into floating number
        print(f"<<< {raw_data} - {unpacked_data}")

        # Converge the model with new input values
        for log in model.convergence_iterator(unpacked_data, limit=50):             # send the unpacked data to the convergence_terator
            await websocket.send(log)
            print(log)

        await websocket.send(model.packed_solution)
        print(f">>> {model.packed_solution} - {tuple(model.solution.flat)}")


async def main():
    ip = "0.0.0.0"
    port = 8765
    print("Starting the computation server")
    async with websockets.serve(evaluation_engine, ip, port):
        print(f" -> Listening on {ip}:{port}")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
