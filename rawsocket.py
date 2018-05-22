import asyncio
import websockets
import json

@asyncio.coroutine
def hello():
    websocket = yield from websockets.connect('wss://api.bitfinex.com/ws/2')
    yield from websocket.send('{"event":"subscribe","channel":"trades","symbol":"BTCUSD"}')
    ack = yield from websocket.recv()
#    print(ack)
    lasttrades = yield from websocket.recv()
#    print(lasttrades)
    while True:
        raw = yield from websocket.recv()
        message = json.loads(raw)
        if message[1] == "tu":
            print(message[2])

asyncio.get_event_loop().run_until_complete(hello())