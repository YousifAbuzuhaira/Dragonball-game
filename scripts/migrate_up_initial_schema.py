"""
Migration script to create the initial database schema.

Creates tables: players, scores, sessions
"""

import sqlite3
import os
import sys


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "game.db")


def migrate_up(db_path=None):
    """Create all tables for the initial schema."""
    if db_path is None:
        db_path = DB_PATH

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                total_wins INTEGER DEFAULT 0,
                total_losses INTEGER DEFAULT 0,
                matches_played INTEGER DEFAULT 0,
                favorite_character TEXT DEFAULT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                character_used TEXT NOT NULL,
                difficulty TEXT DEFAULT 'normal',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players (id)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                character_selected TEXT NOT NULL,
                difficulty TEXT DEFAULT 'normal',
                result TEXT DEFAULT NULL,
                score INTEGER DEFAULT 0,
                started_at TEXT DEFAULT CURRENT_TIMESTAMP,
                ended_at TEXT DEFAULT NULL,
                FOREIGN KEY (player_id) REFERENCES players (id)
            );
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_scores_player_id ON scores (player_id);
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_scores_score_desc ON scores (score DESC);
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_player_id ON sessions (player_id);
        """)

        conn.commit()
        print(f"Migration up completed successfully. Database: {db_path}")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Migration up failed: {e}", file=sys.stderr)
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    migrate_up()