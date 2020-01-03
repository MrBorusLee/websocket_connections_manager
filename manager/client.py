import json

import websockets
import abc
import typing
import dataclasses
import pickle

from yarl import URL

from manager.redis_connection import get_connection

_CLIENTS: typing.Dict[str, typing.Type['BaseWebsocketClient']] = {}


class WebsocketClientException(Exception):
    pass


@dataclasses.dataclass
class ClientDoesNotExistException(WebsocketClientException):
    type_: str

    def __str__(self):
        return f'Client for following url does not exist: {self.type_}'


def get_client(type_: str) -> typing.Type['BaseWebsocketClient']:
    client = _CLIENTS.get(type_)
    if client is None:
        raise ClientDoesNotExistException(type_)
    return client


def _register_client(cls_: typing.Type['BaseWebsocketClient']) -> None:
    _CLIENTS[cls_.TYPE] = cls_


@dataclasses.dataclass
class BaseWebsocketClient(abc.ABC):
    name: str
    url: URL
    connection_attempts: int = 5
    timeout: int = 5
    connection: websockets.WebSocketClientProtocol = dataclasses.field(default=None, init=False)
    status: typing.Optional[str] = dataclasses.field(default=None, init=False)

    TYPE = None

    def as_dict(self):
        return {'url': self.url, 'status': self.status}

    async def loop(self) -> None:
        self.connection = await websockets.connect(str(self.url))  # TODO: implement attempts
        self.status = self.connection.state
        async for message in self.connection:
            await self._handle_message(message)

    async def send_message(self, message: str):
        await self.connection.send(message)

    @abc.abstractmethod
    async def _handle_message(self, message: str) -> None:
        ...


@_register_client
class BitmexInstrumentWebsocketClient(BaseWebsocketClient):
    TYPE = 'bitmex_instrument'

    async def _handle_message(self, message: str) -> None:
        redis_connection = await get_connection()
        message = json.loads(message)

        if 'table' in message:
            data = message['data'][0]

        redis_connection.publish(self.name, pickle.dumps(data))
