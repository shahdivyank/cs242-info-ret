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
                "query": "Cybersecurity Analyst"
            }
        }
    })

print(result)