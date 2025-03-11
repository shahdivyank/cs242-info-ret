from flask import Flask, request
from flask_cors import CORS
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import json
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)

bert = HuggingFaceEmbeddings(
    model_name="google-bert/bert-base-uncased",
)

vectorstore = FAISS.load_local(
    "/Users/shahdivyank/Desktop/CS242/cs242-info-ret/phase_2/bert_index", bert, allow_dangerous_deserialization=True
)

@app.route("/api/query", methods=["GET"])
def query():
    q = request.args.get('q')
    size = request.args.get('size')
    location = request.args.get('location')

    print(q)

    results = vectorstore.similarity_search_with_score(unquote(q), 
                                 k=int(size), 
                                 filter = {'location': unquote(location) } if location else {} 
                                 )
    
    output = []

    for result, score in results:
        print(score, type(score), float(score))
        output.append({
            "score": score.item(),
            "metadata": result.metadata,
            "page_content": result.page_content
        })

    return json.dumps(output)

if __name__ == "__main__":
    app.run()