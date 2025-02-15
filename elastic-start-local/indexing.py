from elasticsearch import Elasticsearch
import json
import sys
import numpy as np
from datetime import datetime
import os


input_file = sys.argv[1]
analyzer_option = sys.argv[2]
print(input_file)
print(analyzer_option)

TOTAL_DOCUMENTS = 137375

times = np.zeros(TOTAL_DOCUMENTS)

if analyzer_option == "remove_stopwords":
    remove_stopwords = True
    print(f"Starting indexing with removing stopwords.")
else:
    remove_stopwords = False
    print(f"Starting indexing without removing stopwords.")

es = Elasticsearch(
  os.getenv("ES_LOCAL_URL"),
  api_key=os.getenv("ES_LOCAL_API_KEY"),
  verify_certs=False
)

stop_words = [
    "and", "the", "is", "in", "at", "of", "on", "for", "to", 
    "a", "an", "with", "from", "by", "about", "as"
]  # keep 'in' or 'with' for certain queries

with open(input_file, "r", encoding="utf-8", errors="ignore") as contents:
    jobs = json.load(contents)

    start = datetime.now()

    for index in range(TOTAL_DOCUMENTS):
        job = jobs[index]
        description = job["Description"]
        if remove_stopwords:
            description = ' '.join([word for word in description.split() if word.lower() not in stop_words])

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

np.save('stopwords.npy', times)