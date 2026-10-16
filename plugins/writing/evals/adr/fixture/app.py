import os

from flask import Flask, abort, jsonify, request

from db import add_item, connect, list_items

app = Flask(__name__)
API_KEY = os.environ["API_KEY"]


@app.before_request
def require_api_key():
    if request.headers.get("X-API-Key", "") != API_KEY:
        abort(401)


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")


@app.get("/items")
def get_items():
    with connect() as conn:
        return jsonify(items=list_items(conn))


@app.post("/items")
def post_item():
    name = (request.get_json(silent=True) or {}).get("name")
    if not name:
        abort(400)
    with connect() as conn:
        return jsonify(id=add_item(conn, name)), 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
