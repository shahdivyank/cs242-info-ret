from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
import json
import numpy as np
from datetime import datetime
from faiss import IndexFlatL2

bert_index = IndexFlatL2(768)

bert = HuggingFaceEmbeddings(
    model_name="google-bert/bert-base-uncased",
)

bert_vectorstore = FAISS(
    embedding_function=bert,
    index=bert_index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

TOTAL_DOCUMENTS = 137375

times = np.zeros(TOTAL_DOCUMENTS)

with open("/Users/shahdivyank/Desktop/CS242/cs242-info-ret/phase_1/data.json", "r", encoding="utf-8", errors="ignore") as contents:
    jobs = json.load(contents)

    times = np.zeros(TOTAL_DOCUMENTS)

    start = datetime.now()

    print("Finished Loading File.")

    for index in range(TOTAL_DOCUMENTS):
        job = jobs[index]

        document = Document(
            id = job["Application Link"],
            page_content = job["Title"] + job["Description"],
            metadata={
                "title": job["Title"], 
                "location": job["Location"], 
                "link": job["Application Link"], 
                "qualification": job["Qualification"], 
                "responsibility": job["Responsibility"]},
        )

        bert_vectorstore.add_documents(documents = [document])

        times[index] = (datetime.now() - start).total_seconds()

np.save('bert_embeddings_indexing.npy', times)
bert_vectorstore.save_local("bert_index")