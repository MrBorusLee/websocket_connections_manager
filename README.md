This is a manger for websocket connections.
### Installation
`pip install git+http://gitlab.southharbour.ru/gogoil/websocket-manager.git`

### Run 
`docker-compose up --build` will run the project.

Connections information is in config.yml, you should specify connection name, connection type and url:
```
BitmexInstrument:
   type: bitmex_instrument
   url: wss://www.bitmex.com/realtime?subscribe=instrument
```

### Available command line commands
To see all available commands use `pipenv run python -m manager --help` from docker container.
