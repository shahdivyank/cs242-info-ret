from elasticsearch import Elasticsearch
import json

es = Elasticsearch(
  "http://localhost:9200",
  api_key="X2NfVTdKUUJWektYUHh1U2FYcWI6d0VJTTJhdjFUNWE3c1pMVWRKX0dPQQ==",
  verify_certs=False
)

result = es.search(index="jobs", query={
        "match": {
            "description": {
                "query": "California"
            }
        }
    })

top_result = result['hits']['hits'][0]['_source']
result = json.dumps(top_result, indent=4)
print(result)