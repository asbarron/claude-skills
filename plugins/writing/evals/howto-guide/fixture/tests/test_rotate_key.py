import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config import ROTATION_GRACE_SECONDS  # noqa: E402


def test_grace_period_is_five_minutes():
    assert ROTATION_GRACE_SECONDS == 300


def test_dry_run_prints_steps_and_writes_nothing(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("API_KEY=abcdef0123456789\n")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "rotate_key.py"), "--dry-run", "--env-file", str(env_file)],
        capture_output=True, text=True, check=True,
    )
    lines = result.stdout.strip().splitlines()
    assert len(lines) == 6
    assert lines[0].startswith("1. would read ")
    assert "300 seconds" in lines[-1]
    assert env_file.read_text() == "API_KEY=abcdef0123456789\n"


def test_real_run_rewrites_env_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("API_KEY=abcdef0123456789\n")
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "rotate_key.py"), "--env-file", str(env_file)],
        capture_output=True, text=True, check=True,
    )
    lines = env_file.read_text().splitlines()
    assert "PREVIOUS_API_KEY=abcdef0123456789" in lines
    assert any(line.startswith("KEY_ROTATED_AT=") for line in lines)
    assert "API_KEY=abcdef0123456789" not in lines
    assert any(line.startswith("API_KEY=") and len(line) == len("API_KEY=") + 64 for line in lines)
