#!/usr/bin/env python3
import argparse
import secrets
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import ENV_FILE, KEY_ROTATED_AT_ENV, PREVIOUS_KEY_ENV, ROTATION_GRACE_SECONDS  # noqa: E402


def read_env(path):
    values = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                key, _, value = line.partition("=")
                values[key.strip()] = value.strip()
    return values


def main(argv=None):
    parser = argparse.ArgumentParser(prog="rotate_key.py", description="Generate a new API key and stage the old one for the grace period.")
    parser.add_argument("--env-file", default=ENV_FILE, help="env file to rewrite (default: %(default)s)")
    parser.add_argument("--dry-run", action="store_true", help="print the steps without writing anything")
    args = parser.parse_args(argv)

    env_path = Path(args.env_file)
    current = read_env(env_path)
    old_key = current.get("API_KEY", "")
    new_key = secrets.token_hex(32)
    rotated_at = int(time.time())

    steps = [
        f"read {env_path}",
        f"set {PREVIOUS_KEY_ENV} to the current API_KEY ({old_key[:6] + '...' if old_key else 'unset'})",
        "set API_KEY to a new 64-character hex key",
        f"set {KEY_ROTATED_AT_ENV} to {rotated_at}",
        f"write {env_path}",
        f"restart the service; the previous key stays valid for {ROTATION_GRACE_SECONDS} seconds",
    ]
    for i, step in enumerate(steps, 1):
        prefix = "would" if args.dry_run else "did"
        print(f"{i}. {prefix} {step}")

    if args.dry_run:
        return 0

    current[PREVIOUS_KEY_ENV] = old_key
    current["API_KEY"] = new_key
    current[KEY_ROTATED_AT_ENV] = str(rotated_at)
    env_path.write_text("".join(f"{k}={v}\n" for k, v in current.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
