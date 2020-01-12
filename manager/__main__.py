import click

from manager.cli import connection
from manager.worker import run_worker


@click.group(name='main')
def main():
    pass


main.add_command(connection)
main.add_command(run_worker)

if __name__ == '__main__':
    main()
