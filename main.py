"""Menu-driven transport booking system."""
import hashlib
import sqlite3
from datetime import date
from create_database import DB_PATH


def hash_password(password):
    """Return a SHA-256 hash for the given password."""
    return hashlib.sha256(password.encode()).hexdigest()


def get_connection():
    """Return a connection to the application database."""
    return sqlite3.connect(DB_PATH)

def login():
    """Log in a user and return the database row if successful."""
    print("\n--- Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    user = cursor.execute(
        "SELECT * FROM user WHERE username = ? AND password = ?",
        (username, hash_password(password)),
    ).fetchone()

    connection.close()

    if user is not None:
        print(f"Welcome back, {username}!")
    else:
        print("Invalid login.")

    return user

def create_account():
    """Create a new ordinary user account."""
    print("\n--- Create Account ---")
    username = input("Choose a username: ")
    password = input("Choose a password: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO user (username, password, admin) VALUES (?, ?, ?)",
        (username, hash_password(password), 0),
    )

    connection.commit()
    connection.close()

    print(f"Account created for '{username}'.")

def view_services():
    """Display all services."""
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    services = cursor.execute(
        "SELECT id, name FROM service ORDER BY id"
    ).fetchall()

    for service in services:
        print(f"{service['id']}: {service['name']}")

    connection.close()


def create_service():
    """Create a new service with buses and runs for the next 7 days."""
    print("\n--- Create New Service ---")
    name = input("Enter service name: ")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO service (name) VALUES (?)", (name,))
    service_id = cursor.lastrowid

    cursor.execute("INSERT INTO bus (model_id, service_id) VALUES (?, ?)", (1, service_id))
    cursor.execute("INSERT INTO bus (model_id, service_id) VALUES (?, ?)", (2, service_id))

    today = date.today()
    for offset in range(7):
        run_date = today.fromordinal(today.toordinal() + offset).isoformat()
        cursor.execute(
            "INSERT INTO run (service_id, date) VALUES (?, ?)",
            (service_id, run_date),
        )

    connection.commit()
    connection.close()

    print(f"Service '{name}' created")

def get_future_runs_for_booking():
    """Return future runs ordered so the newest service appears first."""
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    today_string = date.today().isoformat()

    runs = cursor.execute(
        """
        SELECT run.id, run.date, service.name, service.id AS service_id
        FROM run
        JOIN service ON run.service_id = service.id
        WHERE run.date >= ?
        ORDER BY service.id DESC, run.date ASC, run.id ASC
        """,
        (today_string,),
    ).fetchall()

    connection.close()
    return runs


def view_runs():
    """Display future bus runs for customers."""
    runs = get_future_runs_for_booking()

    for index, run in enumerate(runs, start=1):
        print(f"{index}: {run['name']} on {run['date']}")


def buy_ticket(user_id):
    """Buy tickets for a selected future run."""
    runs = get_future_runs_for_booking()

    print("\n--- Buy Tickets ---")
    print("Select a run by number:")

    for index, run in enumerate(runs, start=1):
        print(f"{index}: {run['name']} on {run['date']}")

    selection_text = input("Enter run number: ")

    try:
        selection = int(selection_text)
    except ValueError:
        print("Invalid run.")
        return

    if selection < 1 or selection > len(runs):
        print("Invalid run.")
        return

    selected_run = runs[selection - 1]

    quantity_text = input("Enter number of tickets (or 'esc' to cancel): ")
    if quantity_text.lower() == "esc":
        print("Booking cancelled.")
        return

    try:
        quantity = int(quantity_text)
    except ValueError:
        print("Invalid number of tickets.")
        return

    if quantity > 50:
        print("Not enough seats available.")
        return

    confirm = input("Press Enter to confirm or type 'esc' to cancel: ")
    if confirm.lower() == "esc":
        print("Booking cancelled.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO ticket (number, user_id, run_id) VALUES (?, ?, ?)",
        (quantity, user_id, selected_run["id"]),
    )

    connection.commit()
    connection.close()

    print("Booking confirmed!")

def view_tickets(user_id):
    """Display tickets belonging to the given user."""
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    tickets = cursor.execute(
        """
        SELECT ticket.number, service.name, run.date
        FROM ticket
        JOIN run ON ticket.run_id = run.id
        JOIN service ON run.service_id = service.id
        WHERE ticket.user_id = ?
        ORDER BY ticket.id
        """,
        (user_id,),
    ).fetchall()

    for ticket in tickets:
        print(f"{ticket['name']} on {ticket['date']}: {ticket['number']} tickets")

    connection.close()


def admin_menu(user):
    """Display the admin menu and process admin actions."""
    while True:
        print("\n--- Admin Menu ---")
        print("1. View services")
        print("2. Create a service")
        print("3. Log out")

        choice = input("Choose an option: ")

        if choice == "1":
            view_services()
        elif choice == "2":
            create_service()
        elif choice == "3":
            return
        else:
            print("Invalid option.")

def user_menu(user):
    """Display the ordinary user menu and process user actions."""
    while True:
        print("\n--- User Menu ---")
        print("1. View future bus runs")
        print("2. Buy tickets")
        print("3. View my tickets")
        print("4. Log out")

        choice = input("Choose an option: ")

        if choice == "1":
            view_runs()
        elif choice == "2":
            buy_ticket(user["id"])
        elif choice == "3":
            view_tickets(user["id"])
        elif choice == "4":
            return
        else:
            print("Invalid option.")

def main():
    """Run the transport booking system."""
    print("=== Transport Booking System ===")

    while True:
        print("\n--- Main Menu ---")
        print("1. Log in")
        print("2. Create account")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            user = login()
            if user is not None:
                if user["admin"] == 1:
                    admin_menu(user)
                else:
                    user_menu(user)
        elif choice == "2":
            create_account()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()