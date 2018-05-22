from elasticsearch import Elasticsearch
import json

es = Elasticsearch(
    ['elastic.koyaan.com'],
    http_auth=('elastic', 'password'),
    scheme="https",
    port=9200,
)

msg = [248307586, 1527023078373, -0.45705041, 8091.1]
doc = {
    "tid": msg[0],
    "timestamp": msg[1],
    "amount": msg[2],
    "price": msg[3]
}

es.index(index="bitfinextradesbtc", doc_type='doc', body=json.dumps(doc))