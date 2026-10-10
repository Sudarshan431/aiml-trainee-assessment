# Task 1: API Data Retrieval and SQLite Storage

## 1. Objective

The objective of this task is to retrieve book information from an external REST API, validate and process the JSON response, store the data in a local SQLite database, and display the stored records.

The application retrieves the following information for each book:
- Book title
- Author name(s)
- First known publication year

## 2. API Used

**Open Library Search API**

- API endpoint: https://openlibrary.org/search.json
- API documentation: https://openlibrary.org/dev/docs/api/search
- HTTP method: `GET`
- Search query: `python programming`
- Maximum results requested: `10`

The API response is returned in JSON format. The application requests only the fields needed for this task: `key`, `title`, `author_name`, and `first_publish_year`.

Note: `first_publish_year` represents the first known publication year of a work and may differ from the publication year of a specific edition.

## 3. Technologies Used

- **Python:** Application logic and data processing
- **Requests:** HTTP requests to the external API
- **SQLite:** Local relational database
- **sqlite3:** Python interface for SQLite
- **Logging:** Application progress and error reporting
- **Pathlib:** Database file path management

## 4. Project Structure

```text
Task-1-API-Retrieval/
├── api_books.py
├── requirements.txt
├── README.md
└── books.db                 # Generated when the application runs
```

The `.venv/` virtual environment is used locally and should not be committed to GitHub.

## 5. Database Schema

The application creates a table named `books` with the following columns:

| Column | Data type | Description |
|---|---|---|
| `id` | INTEGER | Auto-generated local primary key |
| `api_key` | TEXT | Open Library work identifier; unique and required |
| `title` | TEXT | Book title; required |
| `author` | TEXT | Author name(s), stored as comma-separated text |
| `publication_year` | INTEGER | First known publication year; nullable |

The table is created using `CREATE TABLE IF NOT EXISTS`, allowing the application to run repeatedly without recreating an existing table.

The `api_key` column has a unique constraint. An UPSERT statement inserts new books or updates existing records when the same API key is encountered again.

## 6. Implementation

The application is organized into the following functions:

### `fetch_books()`
- Sends a GET request to the Open Library Search API.
- Applies a request timeout and checks HTTP errors.
- Parses and validates the JSON response.
- Skips malformed records and records without a valid title or API key.
- Handles missing authors and publication years.
- Returns a list of cleaned book records.

### `create_database()`
- Connects to the local SQLite database.
- Creates the `books` table if it does not exist.

### `save_books(books)`
- Converts cleaned book dictionaries into database records.
- Uses a parameterized SQL statement to insert or update records.
- Avoids duplicate API identifiers using the unique constraint and UPSERT.

### `display_books()`
- Retrieves stored records using a SQL `SELECT` query.
- Sorts the results by title.
- Displays the title, author, and publication year in a readable console format.
- Displays the total number of retrieved records.

### `main()`
Coordinates database initialization, API retrieval, data storage, display, and handling of expected API, validation, and database errors.

## 7. Setup and Execution

### Prerequisites

- Python 3.10 or a compatible newer Python version
- Internet access to reach the Open Library API

### Step 1: Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
requests>=2.31.0,<3.0
```

SQLite, logging, and pathlib are part of Python's standard library and do not require separate installation.

### Step 3: Run the application

```powershell
python api_books.py
```

On the first successful run, the program creates `books.db`, creates the `books` table, retrieves book records, stores them, and displays the results.

Subsequent runs reuse the database and insert or update records.

## 8. Error Handling and Data Validation

The application includes:
- HTTP status validation using `raise_for_status()`.
- A request timeout to prevent indefinite waiting.
- Validation of the JSON response structure.
- Checks for valid book titles and API identifiers.
- Handling of missing or invalid author and publication-year fields.
- Logging for progress, warnings, and errors.
- Handling of expected request, validation, and SQLite exceptions.

Missing author names or publication years are stored as SQL `NULL` rather than fabricated values.

## 9. Verification and Output

The application was executed successfully in a local Python virtual environment.

Observed during the successful run:
- 10 valid book records fetched from the API.
- 10 records submitted for insertion or update in SQLite.
- Book titles, authors, and publication years retrieved and displayed.
- A total of 10 records displayed in the database query output.

The exact results may vary because the API response can change over time.

To independently verify the number of stored records, run:

```powershell
python -c "import sqlite3; c=sqlite3.connect('books.db'); print('Books stored:', c.execute('SELECT COUNT(*) FROM books').fetchone()[0]); c.close()"
```

Expected count for the verified run: `10`.

## 10. Limitations and Future Improvements

Potential improvements include:
- Adding automated unit tests.
- Implementing retries with exponential backoff for transient network failures.
- Supporting API pagination for larger result sets.
- Adding more detailed validation and structured logging.
- Using a dedicated connection-management pattern for database operations.

## 11. Conclusion

This task demonstrates how to retrieve data from an external REST API, parse and validate JSON, persist records in a relational database, handle duplicate records, and retrieve stored information using SQL.

The implementation provides a simple, repeatable workflow for API integration and local data storage.