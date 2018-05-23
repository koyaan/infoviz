from elasticsearch import Elasticsearch
import json
import os
from dotenv import load_dotenv
import time
import requests

load_dotenv('./.env')

es = Elasticsearch(
    ['elastic.koyaan.com'],
    http_auth=('elastic', os.getenv('ELASTIC_PASSWORD')),
    scheme="https",
    port=9200,
)


# https://docs.bitfinex.com/v2/reference#rest-public-books
url = "https://api.bitfinex.com/v2/book/tBTCUSD/P0?len=100"
while True:
    response = requests.request("GET", url)
    try:
        book = response.json()
        orders = []
        for order in book:
            order_doc = {
                "price": order[0],
                "count": order[1],
                "amount": order[2],
            }
            orders.append(order_doc)
        doc = {
            "book": orders,
            "localtime": int(time.time()*1000)
        }
        print(doc)
        es.index(index="bitfinexbtcbook", doc_type='doc', body=json.dumps(doc))
    except:
        # TODO: log error
        pass
    time.sleep(10) # TODO: fiddle with this