from elasticsearch import Elasticsearch
import json
import numpy as np
from datetime import datetime
import os

es = Elasticsearch(
  os.getenv("ES_LOCAL_URL"),
  api_key=os.getenv("ES_LOCAL_API_KEY"),
  verify_certs=False
)

TOTAL_DOCUMENTS = 137375

times = np.zeros(TOTAL_DOCUMENTS)

with open("data.json", "r") as contents:
    jobs = json.load(contents)

    start = datetime.now()

    for index in range(TOTAL_DOCUMENTS):
        job = jobs[index]

        es.index(
            index="jobs",
            document={
                "title": job["Title"],
                "qualification": job["Qualification"],
                "description": job["Description"],
                "responsibility": job["Responsibility"],
                "link": job["Application Link"],
                "location": job["Location"],
            }
        )

        times[index] = (datetime.now() - start).total_seconds()

np.save('times.npy', times)