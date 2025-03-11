from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


bert = HuggingFaceEmbeddings(
    model_name="google-bert/bert-base-uncased",
)

vectorstore = FAISS.load_local(
    "/Users/shahdivyank/Desktop/CS242/cs242-info-ret/phase_2/bert_index", bert, allow_dangerous_deserialization=True
)


results = vectorstore.search("frontend", k=5, search_type="similarity")

print(results)