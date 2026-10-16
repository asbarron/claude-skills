# Seconds during which the previous API key is still accepted after a rotation.
ROTATION_GRACE_SECONDS = 300

# Environment variables the service reads besides API_KEY.
PREVIOUS_KEY_ENV = "PREVIOUS_API_KEY"
KEY_ROTATED_AT_ENV = "KEY_ROTATED_AT"

# File that `scripts/rotate_key.py` rewrites and that `flask run` loads.
ENV_FILE = ".env"
