import os
import sqlite3


DB_NAME = "flyonwheels.db"


def print_table(cursor: sqlite3.Cursor, table_name: str) -> None:
    """Print all rows from the given table."""
    print("=" * 60)
    print(f"TABLE: {table_name}")
    print("=" * 60)

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    column_names = [column[1] for column in columns_info]
    print("Columns:", ", ".join(column_names))

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    if not rows:
        print("No rows found.\n")
        return

    for row in rows:
        print(row)
    print()


def main() -> None:
    if not os.path.exists(DB_NAME):
        print(f"Database file '{DB_NAME}' does not exist.")
        return

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]

        if not tables:
            print("No tables found in the database.")
            return

        for table_name in tables:
            print_table(cursor, table_name)

    finally:
        connection.close()


if __name__ == "__main__":
    main()