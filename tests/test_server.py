import asyncio
import websockets


STATE = 0
CONNECTIONS = set()


async def increment_state():
    global STATE
    while True:
        STATE += 1
        await asyncio.sleep(3)


async def time(websocket, path):
    CONNECTIONS.add(websocket)
    try:
        while True:
            async for message in websocket:
                print(message)
            await websocket.send(str(STATE))
            await asyncio.sleep(3)
    finally:
        CONNECTIONS.remove(websocket)


start_server = websockets.serve(time, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(asyncio.gather(start_server, increment_state()))
asyncio.get_event_loop().run_forever()
