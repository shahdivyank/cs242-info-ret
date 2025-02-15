from elasticsearch import Elasticsearch
import json
import os

es = Elasticsearch(
  os.getenv("ES_LOCAL_URL"),
  api_key=os.getenv("ES_LOCAL_API_KEY"),
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