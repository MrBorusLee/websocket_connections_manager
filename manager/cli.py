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


@click.option('--message')
@click.option('--connection_name')
@click.command()
def send_message(message, connection_name):
    redis_client = redis.Redis(host=redis_connection.REDIS_HOST, port=redis_connection.REDIS_PORT,
                               db=redis_connection.REDIS_DB)
    redis_client.publish('WS_MESSAGES', pickle.dumps({'message': message, 'connection_name': connection_name}))


connection.add_command(ls)
connection.add_command(send_message)
