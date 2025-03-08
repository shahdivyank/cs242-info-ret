from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

todos = []
todo_id_counter = 1


@app.route("/api/query", methods=["GET"])
def query():
    q = request.args.get('q')

    return request.args

if __name__ == "__main__":
    app.run()