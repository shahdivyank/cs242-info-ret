from elasticsearch import Elasticsearch
import json

es = Elasticsearch(
  "http://localhost:9200",
  api_key="WUZGR0I1VUJvWGQ5UUk0ZngxWkQ6Wm16NVk0M1ZSUTZtQXNSQ01EbEpYUQ==",
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