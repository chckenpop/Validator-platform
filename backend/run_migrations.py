import sqlite3
from pathlib import Path

DB_PATH = Path("data/app.db")
MIGRATION_PATH = Path("migrations/001_init.sql")

def main():
    print("Running migrations...")

    sql = MIGRATION_PATH.read_text()

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()

    print("Migrations applied successfully.")

if __name__ == "__main__":
    main()
