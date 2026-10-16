import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db import add_item, connect, list_items  # noqa: E402


def test_add_and_list_items(tmp_path):
    conn = connect(str(tmp_path / "test.sqlite3"))
    assert add_item(conn, "alpha") == 1
    assert add_item(conn, "bravo") == 2
    assert list_items(conn) == ["alpha", "bravo"]
