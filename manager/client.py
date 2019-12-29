import websockets
import abc
import typing
import dataclasses

from yarl import URL

_CLIENTS: typing.Dict[str, typing.Type['BaseWebsocketClient']] = {}


class WebsocketClientException(Exception):
    pass


@dataclasses.dataclass
class ClientDoesNotExistException(WebsocketClientException):
    url: str

    def __str__(self):
        return f'Client for following url does not exist: {self.url}'


def get_client(url: str) -> typing.Type['BaseWebsocketClient']:
    client = _CLIENTS.get(url)
    if client is None:
        raise ClientDoesNotExistException(url)
    return client


def _register_client(cls_: typing.Type['BaseWebsocketClient']) -> None:
    _CLIENTS[cls_.HOST] = cls_


@dataclasses.dataclass
class BaseWebsocketClient(abc.ABC):
    url: URL
    conn_attempts: int = 5
    conn_timeout: int = 5
    connection: websockets.WebSocketClientProtocol = dataclasses.field(default=None, init=False)
    status: typing.Optional[str] = dataclasses.field(default=None, init=False)

    HOST = None

    def as_dict(self):
        return {'url': self.url, 'status': self.status}

    async def loop(self) -> None:
        self.connection = await websockets.connect(str(self.url))  # TODO: implement attempts
        self.status = self.connection.state
        async for message in self.connection:
            await self._handle_message(message)

    @abc.abstractmethod
    async def _handle_message(self, message: str) -> None:
        ...


@_register_client
class SomeTestWebsocketClient(BaseWebsocketClient):
    HOST = 'localhost'

    async def _handle_message(self, message: str) -> None:
        print(message)
