import sqlite3
import logging
from pathlib import Path

import requests



#configuration
API_URL = "https://openlibrary.org/search.json"
SEARCH_QUERY = "python programming"
RESULT_LIMIT = 10
DB_PATH = Path(__file__).parent / "books.db"
TIMEOUT = 15


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)




# API Retrieval
def fetch_books(query=SEARCH_QUERY, limit=RESULT_LIMIT):
    """Fetch book records from the open Library Search API"""
    params = {
        "q": query,
        "fields": "key,title,author_name,first_publish_year",
        "limit": limit,
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict) or not isinstance(
            data.get("docs"), list
        ):
            raise ValueError("Unexpected API response structure.")

        books = []

        for item in data["docs"]:
            if not isinstance(item, dict):
                continue


            title = item.get("title")
            api_key = item.get("key")


            if not isinstance(title, str) or not title.strip():
                continue
            if not isinstance(api_key, str) or not api_key.strip():
                continue

            authors = item.get("author_name") or []
            if not isinstance(authors, list):
                authors = []

            author = ", ".join(
                str(name).strip()
                for name in authors
                if isinstance(name, str) and name.strip()
            ) or None

            year = item.get("first_publish_year")

            if isinstance(year, bool) or not isinstance(year, int):
                year = None

            books.append({
                "api_key": api_key,
                "title": title.strip(),
                "author": author,
                "publication_year": year
            })

        logger.info("Fetched %d valid book records.", len(books))
        return books


    except  requests.RequestException as exc:
        logger.error("API request failed: %s", exc)
        raise
    except ValueError as exc:
        logger.error("Could not process API response: %s", exc)
        raise





#database setup 
def create_database():
    """Create the database and books table if necessary."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        author TEXT,
        publication_year INTEGER
        )
    """)

    logger.info("Database initialized at %s", DB_PATH)





#store books
def save_books(books):
    """Insert new books or update existing records."""
    if not books:
        logger.warning("No books to save.")
        return 0

    sql = """ 
        INSERT INTO books (
            api_key, title, author, publication_year
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(api_key) DO UPDATE SET
            title = excluded.title,
            author = excluded.author,
            publication_year = excluded.publication_year
    """


    records = [
        (
            book["api_key"],
            book["title"],
            book["author"],
            book["publication_year"],
        )
        for book in books
    ]

    with sqlite3.connect(DB_PATH) as connection:
        connection.executemany(sql, records)

    logger.info("Saved or updated %d records", len(records))
    return len(records)






#display stored books
def display_books():
    """Read saved books from SQLite and display them."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row


        rows = connection.execute("""
            SELECT title, author, publication_year
            FROM books
            ORDER BY title COLLATE NOCASE
        """).fetchall()


    if not rows:
        print("\nNo books found in the database.")
        return


    print(f"\n{'TITLE:<45'} {'AUTHOR':<30} {'YEAR':<6}")
    print("-" * 85)


    for row in rows:
        title = row["title"] or "Unknown"
        author = row["author"] or "Unknown"
        year = (
            str(row["publication_year"])
            if row["publication_year"] is not None
            else "Unknown"
        )


        print(f"{title[:43]:<45} {author[:28]:<30} {year:<6}")

    print(f"\nTotal books in database: {len(rows)}")





#main
def main():
    print("=== Book Data Retrieval and storage ===")


    try:
        create_database()
        books = fetch_books()

        if books:
            save_books(books)
        else:
            logger.warning(
                "The API returned no valid books, displaying existing records."
            )


        display_books()


    except (requests.RequestException, ValueError, sqlite3.Error) as exc:
        logger.error("Task failed: %s", exc)
        raise SystemExit(1)


if __name__ == "__main__":
    main()