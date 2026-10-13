
import csv
import sqlite3
from pathlib import Path

CSV_FILE = Path(__file__).with_name("users.csv")
DB_FILE = Path(__file__).with_name("users.db")


def import_users():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

    required_columns = {"user_id", "name", "email", "age", "city"}

    with CSV_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                f"CSV must contain these columns: {sorted(required_columns)}"
            )

        users = []

        for line_number, row in enumerate(reader, start=2):
            try:
                user_id = int(row["user_id"])
                name = row["name"].strip()
                email = row["email"].strip().lower()
                age = int(row["age"])
                city = row["city"].strip()

                if user_id <= 0 or age <= 0:
                    raise ValueError("user_id and age must be positive")

                if not name or not email or not city:
                    raise ValueError("name, email, and city cannot be empty")

                users.append((user_id, name, email, age, city))

            except (ValueError, TypeError) as error:
                raise ValueError(
                    f"Invalid data on CSV line {line_number}: {error}"
                ) from error

        with sqlite3.connect(DB_FILE) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    age INTEGER NOT NULL CHECK (age > 0),
                    city TEXT NOT NULL
                )
            """)

            connection.executemany("""
                INSERT INTO users (user_id, name, email, age, city)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    name = excluded.name,
                    email = excluded.email,
                    age = excluded.age,
                    city = excluded.city
            """, users)

            rows = connection.execute("""
                SELECT user_id, name, email, age, city
                FROM users
                ORDER BY user_id
            """).fetchall()

    print(f"Successfully imported {len(users)} CSV rows.")
    print(f"Database: {DB_FILE.name}\n")
    print(f"{'ID':<5}{'NAME':<20}{'EMAIL':<28}{'AGE':<6}CITY")
    print("-" * 75)

    for user_id, name, email, age, city in rows:
        print(f"{user_id:<5}{name:<20}{email:<28}{age:<6}{city}")


if __name__ == "__main__":
    try:
        import_users()
    except (OSError, sqlite3.Error, ValueError, csv.Error) as error:
        print(f"Import failed: {error}")
        raise SystemExit(1)
