from elasticsearch import Elasticsearch
import asyncio
import websockets
import json
import os
from dotenv import load_dotenv
import certifi

load_dotenv('./.env')

@asyncio.coroutine
def hello():
    es = Elasticsearch(
        ['elastic.koyaan.com'],
        http_auth=('elastic', os.getenv('ELASTIC_PASSWORD')),
        scheme="https",
        port=9200,
    )

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
            msg = message[2]
            print(msg)
            doc = {
                "tid": msg[0],
                "timestamp": msg[1],
                "amount": msg[2],
                "price": msg[3]
            }
            es.index(index="bitfinextradesbtc", doc_type='doc', body=json.dumps(doc))

asyncio.get_event_loop().run_until_complete(hello())