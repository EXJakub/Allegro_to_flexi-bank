from __future__ import annotations

import sqlite3
from dataclasses import dataclass


@dataclass
class Cursor:
    occurred_at: str
    movement_id: str


class StateStore:
    def __init__(self, db_path: str):
        self._conn = sqlite3.connect(db_path)
        self._initialize()

    def _initialize(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sync_cursor (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                occurred_at TEXT NOT NULL,
                movement_id TEXT NOT NULL
            )
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_movements (
                movement_id TEXT PRIMARY KEY,
                occurred_at TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def get_cursor(self) -> Cursor | None:
        row = self._conn.execute(
            "SELECT occurred_at, movement_id FROM sync_cursor WHERE id = 1"
        ).fetchone()
        if not row:
            return None
        return Cursor(occurred_at=row[0], movement_id=row[1])

    def save_cursor(self, occurred_at: str, movement_id: str) -> None:
        self._conn.execute(
            """
            INSERT INTO sync_cursor (id, occurred_at, movement_id)
            VALUES (1, ?, ?)
            ON CONFLICT(id) DO UPDATE SET occurred_at=excluded.occurred_at, movement_id=excluded.movement_id
            """,
            (occurred_at, movement_id),
        )
        self._conn.commit()

    def was_processed(self, movement_id: str) -> bool:
        row = self._conn.execute(
            "SELECT 1 FROM processed_movements WHERE movement_id = ?",
            (movement_id,),
        ).fetchone()
        return bool(row)

    def mark_processed(self, movement_id: str, occurred_at: str) -> None:
        self._conn.execute(
            "INSERT OR IGNORE INTO processed_movements (movement_id, occurred_at) VALUES (?, ?)",
            (movement_id, occurred_at),
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()
