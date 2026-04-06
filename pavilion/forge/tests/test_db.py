import pytest
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import init_db, get_connection


def test_init_creates_tables(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    assert "participants" in tables
    assert "sessions" in tables
    assert "pods" in tables
    assert "pod_members" in tables
    assert "forge_leaders" in tables
    assert "session_participants" in tables
    assert "touchpoints" in tables
    conn.close()


def test_get_connection_returns_row_factory(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    conn = get_connection(db_path)
    conn.execute("INSERT INTO sessions VALUES ('s1', 'ai-gtm', 1, 8, '2026-04-29', NULL, NULL)")
    conn.commit()
    row = conn.execute("SELECT * FROM sessions WHERE id='s1'").fetchone()
    assert row["id"] == "s1"
    assert row["course_id"] == "ai-gtm"
    conn.close()
