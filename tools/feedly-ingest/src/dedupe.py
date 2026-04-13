"""SQLite-backed seen store: url -> file path, content hash, fetched_at."""
from __future__ import annotations

import sqlite3
import threading
from datetime import datetime
from pathlib import Path


class SeenStore:
    """Thread-safe dedupe store.

    SQLite's Python bindings pin each connection to the thread that created it
    unless ``check_same_thread=False``. We opt in and serialise reads/writes
    with a lock so multiple ingest workers can share a single store.
    """

    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._lock = threading.Lock()
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS seen (
                url          TEXT PRIMARY KEY,
                path         TEXT NOT NULL,
                content_hash TEXT,
                fetched_at   TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def contains(self, url: str) -> bool:
        with self._lock:
            cur = self.conn.execute("SELECT 1 FROM seen WHERE url = ?", (url,))
            return cur.fetchone() is not None

    def add(self, url: str, path: Path, content_hash: str | None = None) -> None:
        with self._lock:
            self.conn.execute(
                "INSERT OR REPLACE INTO seen(url, path, content_hash, fetched_at) "
                "VALUES (?, ?, ?, ?)",
                (url, str(path), content_hash, datetime.utcnow().isoformat()),
            )
            self.conn.commit()

    def close(self) -> None:
        with self._lock:
            self.conn.close()
