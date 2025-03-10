from flask import Flask, request
from flask_cors import CORS
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import json

app = Flask(__name__)
CORS(app)

bert = HuggingFaceEmbeddings(
    model_name="google-bert/bert-base-uncased",
)

vectorstore = FAISS.load_local(
    "/Users/shahdivyank/Desktop/cs242-info-ret/phase_2/bert_index", bert, allow_dangerous_deserialization=True
)

@app.route("/api/query", methods=["GET"])
def query():
    q = request.args.get('q')

    results = vectorstore.search(q, k=5, search_type="similarity")

    output = []

    for result in results:
        output.append({
            "metadata": result.metadata,
            "page_content": result.page_content
        })

    return json.dumps(output)

if __name__ == "__main__":
    app.run()