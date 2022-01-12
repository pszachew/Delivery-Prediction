#!/usr/bin/env python3

from flask import Flask, request, json

app = Flask(__name__)


def process_data(data: dict) -> dict:
    name = request.json["name"]
    response_data = {"name": name, "url": "www"}
    return response_data


@app.route('/', methods=["GET"])
def process_request():
    if request.method == "GET":
        if request.get_json(force=True):
            print("Got request: ", request.json)
            response = process_data(request.json)
            return json.jsonify(response)
        else:
            return "Missing json"


if __name__ == '__main__':
    app.run()
