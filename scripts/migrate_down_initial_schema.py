"""Migration script to drop all database tables (rollback initial schema)."""

import sqlite3
import os
import sys


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "game.db")


def migrate_down(db_path=None):
    """Drop all tables created by the initial schema migration.

    Args:
        db_path: Optional path to the SQLite database file.
                 Defaults to game.db in the project root.
    """
    if db_path is None:
        db_path = DB_PATH

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    tables_to_drop = ["sessions", "scores", "players"]

    try:
        for table_name in tables_to_drop:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Dropped table: {table_name}")

        connection.commit()
        print("Migration down completed successfully.")
    except sqlite3.Error as e:
        connection.rollback()
        print(f"Migration down failed: {e}")
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    custom_db_path = sys.argv[1] if len(sys.argv) > 1 else None
    migrate_down(custom_db_path)