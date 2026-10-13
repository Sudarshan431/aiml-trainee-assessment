# Task 3: CSV to SQLite Database

## Overview
This project imports user information from a CSV file into an SQLite database using Python. It validates the input data, stores the records in a database, and displays the imported users in the terminal.

## Technologies Used
- Python 3
- CSV module
- SQLite3
- pathlib

## Project Structure

```text
Task-3-CSV-to-SQLite/
├── users.csv
├── import_users.py
├── users.db
└── README.md
```

## CSV File Format

The `users.csv` file contains the following columns:

| Column | Description |
|---|---|
| `user_id` | Unique identifier for each user |
| `name` | User's full name |
| `email` | User's email address |
| `age` | User's age |
| `city` | User's city |

## Features

- Reads user records from a CSV file.
- Validates required column names and input values.
- Checks that user IDs and ages are positive.
- Rejects empty names, email addresses, and cities.
- Creates an SQLite database and a `users` table if they do not already exist.
- Uses parameterized SQL queries to insert data safely.
- Updates existing records when their `user_id` conflicts with an existing record.
- Enforces unique email addresses and positive ages through database constraints.
- Displays the stored user records in the terminal.
- Handles file, CSV, validation, and SQLite errors.

## Prerequisites

- Python 3 installed on your system.
- No external Python packages are required.

## How to Run

1. Open a terminal in the `Task-3-CSV-to-SQLite` directory.
2. Ensure that `users.csv` is present.
3. Run the following command:

```bash
python import_users.py
```

The script validates the CSV data, imports the records into `users.db`, and displays the users in the terminal.

## Expected Output

```text
Successfully imported 5 CSV rows.
Database: users.db

ID   NAME                EMAIL                       AGE   CITY
---------------------------------------------------------------------------
1    Aarav Sharma        aarav@example.com           22    Pune
2    Priya Patel         priya@example.com           24    Mumbai
3    Rohan Verma         rohan@example.com           21    Nashik
4    Neha Joshi          neha@example.com            23    Pune
5    Aditya Singh        aditya@example.com          25    Nagpur
```

*The output above is based on the current sample CSV data.*

## Database Schema

The SQLite database contains a `users` table with these columns:

- `user_id`: Integer primary key.
- `name`: Required text field.
- `email`: Required unique text field.
- `age`: Required integer greater than zero.
- `city`: Required text field.

## Error Handling

The script reports errors for missing files, invalid CSV structure, invalid user data, CSV parsing issues, and database errors. Invalid CSV records stop the import and display the relevant line number.

## Author

Sudarshan Mali
