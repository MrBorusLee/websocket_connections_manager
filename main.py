import asyncio
from manager.manager import WsConnectionsManager
import yaml
from collections import ChainMap

with open('config.yml') as f:
    data = yaml.load(f)


manager = WsConnectionsManager()
for connection_name, connection_data in data['connections'].items():
    connection_kwargs = ChainMap(connection_data, data)
    manager.create_connection(connection_name, connection_kwargs['type'], connection_kwargs['url'],
                              timeout=connection_kwargs['timeout'])


asyncio.get_event_loop().run_until_complete(manager.gather_loops())
