import dataclasses
import typing
import asyncio
import pickle

from yarl import URL

from manager.client import BaseWebsocketClient, get_client
from manager.redis_connection import get_connection


@dataclasses.dataclass
class WsConnectionsManager:
    connections: typing.Dict[str, BaseWebsocketClient] = dataclasses.field(default_factory=dict)

    def create_connection(self, name: str, type_: str, url: str, **params):
        url = URL(url)
        ws_client_class = get_client(type_)
        ws_client = ws_client_class(url=url, name=name, **params)
        self.connections[name] = ws_client

    async def update_connection_statuses(self):
        while True:
            data = {}
            for url, client in self.connections.items():
                data[url] = client.as_dict()
            redis = await get_connection()
            await redis.set('CONNECTIONS', pickle.dumps(data), expire=15)
            await asyncio.sleep(10)

    async def send_messages_from_command_line(self):
        redis = await get_connection()
        channel, = await redis.subscribe('WS_MESSAGES')

        async for message in channel.iter():
            message = pickle.loads(message)
            await self.connections[message['connection_name']].send_message(message['message'])

    def gather_loops(self):
        return asyncio.gather(
            *[client.loop() for client in self.connections.values()] + [self.update_connection_statuses(),
                                                                        self.send_messages_from_command_line()]
        )
