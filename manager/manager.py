import dataclasses
import typing
import asyncio
import pickle

from yarl import URL

from manager.client import BaseWebsocketClient, get_client
from manager.redis_connection import get_connection


@dataclasses.dataclass
class WsConnectionsManager:
    connections: typing.Dict[URL, BaseWebsocketClient] = dataclasses.field(default_factory=dict)

    def add_connection(self, url: str):
        url = URL(url)
        ws_client_class = get_client(url.host)
        ws_client = ws_client_class(url)
        self.connections[url] = ws_client

    async def update_connection_statuses(self):
        while True:
            data = {}
            for url, client in self.connections.items():
                data[url] = client.as_dict()
            redis = await get_connection()
            await redis.set('CONNECTIONS', pickle.dumps(data), expire=15)
            await asyncio.sleep(10)

    def gather_loops(self):
        return asyncio.gather(
            *[client.loop() for client in self.connections.values()] + [self.update_connection_statuses()]
        )
