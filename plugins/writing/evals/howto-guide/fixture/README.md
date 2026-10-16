# items-service

A small Flask service that lists items behind an API key.

## Install

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Verified with Python 3.12 and Flask 3.1.0.

## Run

The service reads `API_KEY` from the environment and rejects any request whose `X-API-Key` header does not match it.

```sh
API_KEY=REPLACE_WITH_YOUR_KEY flask --app app run --port 8080
curl -H 'X-API-Key: REPLACE_WITH_YOUR_KEY' http://127.0.0.1:8080/items
```

Expected output:

```json
{"items":["alpha","bravo","charlie"]}
```

A request with a missing or wrong key returns `401`.

## Test

```sh
python3 -m pytest -q
```

## License

MIT
