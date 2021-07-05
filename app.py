from flask import Flask, Response, jsonify, render_template, send_from_directory, request, session
import json
from src.main import get_query_engine
from os import listdir
from os.path import isfile, join

app = Flask(__name__, template_folder= "")
app.static_folder = "static"

@app.route("/search", methods=['POST'])
def search():
    engine = get_query_engine(build=False)
    if (not request.is_json):
        c = json.loads(request.data)['values']
    else:
        c = json.loads(request.data)
    tweets = engine.search(c['query'])
    json_msg = json.dumps(tweets)
    return Response(json_msg, status=201, mimetype="application/json")

@app.route('/', methods=['GET'])
def index():
    return render_template('/static/html/index.html')

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))