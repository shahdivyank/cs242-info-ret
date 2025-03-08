from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
import json
import numpy as np
from datetime import datetime

bert_index = faiss.IndexFlatL2(768)

bert = HuggingFaceEmbeddings(
    model_name="google-bert/bert-base-uncased",
)

bert_vectorstore = FAISS(
    embedding_function=bert,
    index=bert_index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)