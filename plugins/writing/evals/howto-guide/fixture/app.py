import os
import time

from flask import Flask, abort, jsonify, request

from config import KEY_ROTATED_AT_ENV, PREVIOUS_KEY_ENV, ROTATION_GRACE_SECONDS

app = Flask(__name__)

API_KEY = os.environ["API_KEY"]
PREVIOUS_API_KEY = os.environ.get(PREVIOUS_KEY_ENV)
KEY_ROTATED_AT = float(os.environ.get(KEY_ROTATED_AT_ENV, "0"))


def key_is_valid(presented):
    if presented == API_KEY:
        return True
    if PREVIOUS_API_KEY and presented == PREVIOUS_API_KEY:
        return time.time() - KEY_ROTATED_AT <= ROTATION_GRACE_SECONDS
    return False


@app.before_request
def require_api_key():
    if not key_is_valid(request.headers.get("X-API-Key", "")):
        abort(401)


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")


@app.get("/items")
def list_items():
    return jsonify(items=["alpha", "bravo", "charlie"])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
