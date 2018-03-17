import flask
import json
from flask import jsonify, request
from src.youtube_data import Youtube_data
youtube_data = Youtube_data()

app = flask.Flask(__name__) 
app.secret_key = "REPLACE ME"

@app.route('/')
def index():
    return jsonify({"status": "running"})


@app.route('/youtube_data', methods=['POST'])
def youtube_collect():
    args = json.loads(request.data)

    topics = args['topics']
    filters = args['filters']
    result = youtube_data.search(
        topics, filters)
    return jsonify(result)
  
if __name__== '__main__':
    app.run("localhost", 8090, debug=True)
