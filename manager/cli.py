import click
import redis
import pickle

from manager import redis_connection


@click.group(name='connection')
def connection():
    pass


@click.command()
def ls():
    redis_client = redis.Redis(host=redis_connection.REDIS_HOST, port=redis_connection.REDIS_PORT,
                               db=redis_connection.REDIS_DB)
    data = redis_client.get('CONNECTIONS')
    if not data:
        return
    connections = pickle.loads(redis_client.get('CONNECTIONS'))
    for websocket_connection in connections.items():
        print(websocket_connection)


connection.add_command(ls)
