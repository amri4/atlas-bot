import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "atlas.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT NOT NULL,
                challenger_id TEXT NOT NULL,
                opponent_id TEXT NOT NULL,
                winner_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS punches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT NOT NULL,
                puncher_id TEXT NOT NULL,
                victim_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def add_fight(guild_id, challenger_id, opponent_id, winner_id):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO fights (guild_id, challenger_id, opponent_id, winner_id) VALUES (?, ?, ?, ?)",
            (str(guild_id), str(challenger_id), str(opponent_id), str(winner_id)),
        )
        conn.commit()


def add_punch(guild_id, puncher_id, victim_id):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO punches (guild_id, puncher_id, victim_id) VALUES (?, ?, ?)",
            (str(guild_id), str(puncher_id), str(victim_id)),
        )
        conn.commit()


def get_fight_scores(guild_id, limit=5):
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT winner_id, COUNT(*) as wins
            FROM fights
            WHERE guild_id = ?
            GROUP BY winner_id
            ORDER BY wins DESC
            LIMIT ?
            """,
            (str(guild_id), limit),
        ).fetchall()
    return rows


def get_punch_counts(guild_id, limit=5):
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT puncher_id, COUNT(*) as punches
            FROM punches
            WHERE guild_id = ?
            GROUP BY puncher_id
            ORDER BY punches DESC
            LIMIT ?
            """,
            (str(guild_id), limit),
        ).fetchall()
    return rows
