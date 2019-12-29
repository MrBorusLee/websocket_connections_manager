import asyncio
from manager.manager import WsConnectionsManager

manager = WsConnectionsManager()
for i in range(3):
    manager.add_connection(f'ws://localhost:5678/{i}')


asyncio.get_event_loop().run_until_complete(manager.gather_loops())
