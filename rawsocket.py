import asyncio
import websockets

@asyncio.coroutine
def hello():
    websocket = yield from websockets.connect('wss://api.bitfinex.com/ws/2')
    yield from websocket.send('{"event":"subscribe","channel":"trades","symbol":"BTCUSD"}')
    greeting = yield from websocket.recv()
    print("< %s " % greeting)
    while True:
        message = yield from websocket.recv()
        print(message)

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()