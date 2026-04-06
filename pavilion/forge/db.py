import sqlite3
from config import DATABASE_PATH


def get_connection(db_path=DATABASE_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=DATABASE_PATH):
    conn = get_connection(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            course_id TEXT NOT NULL,
            session_number INTEGER NOT NULL,
            total_sessions INTEGER NOT NULL,
            session_date TEXT,
            transcript_path TEXT,
            processed_at TEXT
        );

        CREATE TABLE IF NOT EXISTS participants (
            id TEXT PRIMARY KEY,
            cohort_id TEXT NOT NULL,
            name TEXT,
            email TEXT,
            title TEXT,
            company TEXT,
            stage TEXT,
            function TEXT,
            hive_bright_id TEXT
        );

        CREATE TABLE IF NOT EXISTS session_participants (
            session_id TEXT NOT NULL,
            participant_id TEXT NOT NULL,
            attended INTEGER DEFAULT 1,
            duration_minutes INTEGER,
            contribution_score REAL DEFAULT 0.0,
            notable_moment TEXT,
            PRIMARY KEY (session_id, participant_id)
        );

        CREATE TABLE IF NOT EXISTS forge_leaders (
            participant_id TEXT PRIMARY KEY,
            cohort_id TEXT NOT NULL,
            nominated_at_session INTEGER,
            reason TEXT
        );

        CREATE TABLE IF NOT EXISTS pods (
            id TEXT PRIMARY KEY,
            cohort_id TEXT NOT NULL,
            formed_at_session INTEGER,
            function TEXT,
            stage TEXT
        );

        CREATE TABLE IF NOT EXISTS pod_members (
            pod_id TEXT NOT NULL,
            participant_id TEXT NOT NULL,
            is_wildcard INTEGER DEFAULT 0,
            PRIMARY KEY (pod_id, participant_id)
        );

        CREATE TABLE IF NOT EXISTS touchpoints (
            id TEXT PRIMARY KEY,
            participant_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            type TEXT NOT NULL,
            content TEXT,
            sent_at TEXT,
            slack_channel TEXT
        );
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DATABASE_PATH}")
