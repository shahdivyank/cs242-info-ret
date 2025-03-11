from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
import json
import numpy as np
from datetime import datetime
import faiss

bert_index = faiss.IndexFlatL2(768)
bert = HuggingFaceEmbeddings(model_name="google-bert/bert-base-uncased")

bert_vectorstore = FAISS(
    embedding_function=bert,
    index=bert_index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

with open("/Users/shahdivyank/Desktop/CS242/cs242-info-ret/phase_1/data.json", "r", encoding="utf-8", errors="ignore") as contents:
    jobs = json.load(contents)

TOTAL_DOCUMENTS = len(jobs)
BATCH_SIZE = 1000
times = np.zeros(TOTAL_DOCUMENTS)
start = datetime.now()

print(f"Starting indexing of {TOTAL_DOCUMENTS} documents in batches of {BATCH_SIZE}...")
for i in range(0, TOTAL_DOCUMENTS, BATCH_SIZE):
    batch_jobs = jobs[i : i + BATCH_SIZE]

    documents = [
        Document(
            id = job["Application Link"],
            page_content = job["Title"] + job["Description"],
            metadata={
                "title": job["Title"], 
                "location": job["Location"], 
                "link": job["Application Link"], 
                "qualification": job["Qualification"], 
                "responsibility": job["Responsibility"]},
        )
        for job in batch_jobs
    ]

    bert_vectorstore.add_documents(documents=documents)
    times[i : i + len(batch_jobs)] = (datetime.now() - start).total_seconds()
    print(f"Indexed {i + len(batch_jobs)}/{TOTAL_DOCUMENTS} documents.")

np.save("bert_embeddings_batches_indexing.npy", times)

bert_vectorstore.save_local("bert_index_batches")

print("Indexing complete. Saved FAISS index and metadata.")
