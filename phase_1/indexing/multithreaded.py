from elasticsearch import Elasticsearch
import json
import numpy as np
from datetime import datetime
import threading

es = Elasticsearch(
  "http://localhost:9200",
  api_key="WUZGR0I1VUJvWGQ5UUk0ZngxWkQ6Wm16NVk0M1ZSUTZtQXNSQ01EbEpYUQ==",
  verify_certs=False
)

def split_array(A, count):
        quotient = A.shape[0] // count
        remainder = A.shape[0] % count

        splits = [(i + 1) * quotient + min(i + 1, remainder) for i in range(count - 1)]
        
        return np.split(A, splits)


def task(values, jobs, i, thread_times, thread_index):
    start = datetime.now()

    for index in values:
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

    thread_times[thread_index][i] = (datetime.now() - start).total_seconds()

TOTAL_DOCUMENTS = 137375

counts = np.arange(0, TOTAL_DOCUMENTS)

THREADS = [2, 3, 4, 5, 8, 10]
thread_times = np.zeros((len(THREADS), max(THREADS)))

for thread_index in range(len(THREADS)):
    THREAD = THREADS[thread_index]

    splits = split_array(counts, THREAD)

    threads = []

    with open("data.json", "r") as contents:
        jobs = json.load(contents)

        for index in range(THREAD):
            values = splits[index]
            thread = threading.Thread(target=task, args=(values, jobs, index, thread_times, thread_index))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()


    np.save('multithreaded.npy', thread_times)