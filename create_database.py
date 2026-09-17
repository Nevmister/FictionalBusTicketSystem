"""Create and populate the flyonwheels SQLite database."""
import hashlib
import sqlite3
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path("flyonwheels.db")


def hash_password(password):
    """Return the SHA-256 hash of a password string."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_database():
    """Create the database and populate it with starter data."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.executescript(
        """
        DROP TABLE IF EXISTS ticket;
        DROP TABLE IF EXISTS run;
        DROP TABLE IF EXISTS bus;
        DROP TABLE IF EXISTS bus_model;
        DROP TABLE IF EXISTS service;
        DROP TABLE IF EXISTS user;

        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            admin BOOLEAN NOT NULL
        );

        CREATE TABLE service (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE bus_model (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            seats INTEGER NOT NULL
        );

        CREATE TABLE bus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            model_id INTEGER NOT NULL,
            FOREIGN KEY (service_id) REFERENCES service(id),
            FOREIGN KEY (model_id) REFERENCES bus_model(id)
        );

        CREATE TABLE run (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (service_id) REFERENCES service(id)
        );

        CREATE TABLE ticket (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            run_id INTEGER NOT NULL,
            number INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (run_id) REFERENCES run(id)
        );
        """
    )

    cursor.execute(
        "INSERT INTO user (username, password, admin) VALUES (?, ?, ?)",
        ("Bob", hash_password("pqr123#!"), 1),
    )

    service_names = [
        "Dublin to Kilkenny, 7pm",
        "Dublin to Letterkenny, 8am",
        "Dublin to Wicklow, 6pm",
    ]
    for service_name in service_names:
        cursor.execute("INSERT INTO service (name) VALUES (?)", (service_name,))

    cursor.execute(
        "INSERT INTO bus_model (name, seats) VALUES (?, ?)",
        ("A", 30),
    )
    cursor.execute(
        "INSERT INTO bus_model (name, seats) VALUES (?, ?)",
        ("B", 50),
    )

    for service_id in range(1, 4):
        cursor.execute(
            "INSERT INTO bus (service_id, model_id) VALUES (?, ?)",
            (service_id, 1),
        )
        cursor.execute(
            "INSERT INTO bus (service_id, model_id) VALUES (?, ?)",
            (service_id, 2),
        )

    today = date.today()
    for service_id in range(1, 4):
        for offset in range(7):
            run_date = (today + timedelta(days=offset)).isoformat()
            cursor.execute(
                "INSERT INTO run (service_id, date) VALUES (?, ?)",
                (service_id, run_date),
            )

    next_day = (today + timedelta(days=1)).isoformat()
    letterkenny_run = cursor.execute(
        """
        SELECT run.id
        FROM run
        JOIN service ON run.service_id = service.id
        WHERE service.name = ? AND run.date = ?
        """,
        ("Dublin to Letterkenny, 8am", next_day),
    ).fetchone()

    cursor.execute(
        "INSERT INTO ticket (user_id, run_id, number) VALUES (?, ?, ?)",
        (1, letterkenny_run[0], 1),
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()