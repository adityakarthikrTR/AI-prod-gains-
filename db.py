import os
import sqlite3
import datetime as dt
from typing import List, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

def _conn():
    return sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with _conn() as cx:
        cx.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                name TEXT NOT NULL,
                prod_gain TEXT,
                dotted_gain TEXT,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (name, start_date, end_date)
            )
        """)

def get_entries(start_date, end_date):
    s = start_date.isoformat()
    e = end_date.isoformat()
    with _conn() as cx:
        cur = cx.execute("""
            SELECT name, prod_gain, dotted_gain
            FROM entries
            WHERE start_date = ? AND end_date = ?
            ORDER BY name COLLATE NOCASE
        """, (s, e))
        return [(row[0], row[1] or "", row[2] or "") for row in cur.fetchall()]

def upsert_entries(start_date, end_date, records: List[Dict]):
    s = start_date.isoformat()
    e = end_date.isoformat()
    now = dt.datetime.utcnow().isoformat()
    with _conn() as cx:
        for rec in records:
            name = (rec.get("Name of the leader") or "").strip()
            prod = (rec.get("Productivity Gains (In Hours)") or "").strip()
            dotted = (rec.get("+ Productivity Gains (Dotted Team) (In Hours)") or "").strip()
            if not name:
                continue
            cx.execute("""
                INSERT INTO entries (name, prod_gain, dotted_gain, start_date, end_date, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(name, start_date, end_date)
                DO UPDATE SET
                    prod_gain=excluded.prod_gain,
                    dotted_gain=excluded.dotted_gain,
                    updated_at=excluded.updated_at
            """, (name, prod, dotted, s, e, now))

def delete_entries_not_in(start_date, end_date, keep_names: List[str]):
    s = start_date.isoformat()
    e = end_date.isoformat()
    keep_names = [n.strip() for n in keep_names if n and n.strip()]
    with _conn() as cx:
        if keep_names:
            placeholders = ",".join("?" for _ in keep_names)
            cx.execute(f"""
                DELETE FROM entries
                WHERE start_date = ? AND end_date = ?
                  AND name NOT IN ({placeholders})
            """, [s, e, *keep_names])
        else:
            cx.execute("""
                DELETE FROM entries
                WHERE start_date = ? AND end_date = ?
            """, (s, e))
