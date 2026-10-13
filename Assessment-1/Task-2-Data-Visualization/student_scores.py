import logging
from pathlib import Path

import requests
import pandas as pd
import matplotlib.pyplot as plt



#configuration
API_URL = "http://127.0.0.1:5000/api/student-scores"
Timeout = 15

OUTPUT_DIR = Path(__file__).parent
CHART_PATH = OUTPUT_DIR / "average_scores.png"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)



def fetch_student_scores():
    """Fetch student scores from a REST API."""
    try:
        response = requests.get(API_URL, timeout=Timeout)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict) or not isinstance(
            data.get("students"), list
        ):
            raise ValueError(
                "API response must contain a 'students' list."
            )

        logger.info("Successfully fetched student data.")
        return data["students"]

    except requests.RequestException as exc:
        logger.error("API request failed: %s", exc)
        raise
    except ValueError as exc:
        logger.error("Invalid API response: %s", exc)
        raise


def calculate_averages(students):
    """Validate scores and calculate each students's average."""
    records = []

    for student in students:
        if not isinstance(student, dict):
            logger.warning("Skipping invalid student record.")
            continue

        name = student.get("name")
        scores = student.get("scores")

        if not isinstance(name, str) or not name.strip():
            logger.warning("Skipping record with missing name.")
            continue

        if not isinstance(scores, dict) or not scores:
            logger.warning("Skipping %s: no scores.", name)
            continue


        valid_scores = []

        for subject, score in scores.items():
            #rejecting booleans, strings, missing values, and invalid scores
            if (
                isinstance(score, bool)
                or not isinstance(score, (int, float))
                or not 0 <= score <=  100
            ):
                logger.warning(
                    "Ignoring invalid score for %s: %s",
                    name, subject
                )
                continue

            valid_scores.append(score)

        if not valid_scores:
            logger.warning("Skipping %s: no valid scores.", name)
            continue

        records.append({
            "Student": name.strip(),
            "Average Score": sum(valid_scores) / len(valid_scores)
        })

    if not records:
        raise ValueError("No valid student scores were found.")

    return pd.DataFrame(records)


def display_results(df):
    """Display student averages in the terminal."""
    print("\n=== Student Average Scores ===\n")
    print(df.to_string(
        index=False,
        formatters={"Average Score": "{:2f}".format}
    ))


def create_chart(df):
    """Generate and save a bar chart of average scores."""
    ordered = df.sort_values(
        "Average Score", ascending=False
    )

    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        ordered["Student"],
        ordered["Average Score"]
    )

    plt.bar_label(
        bars,
        fmt="%.1f",
        padding=3
    )
    plt.title("Average Test Scores by Student")
    plt.xlabel("Student")
    plt.ylabel("Average Score")
    plt.ylim(0, 110)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    plt.savefig(CHART_PATH, dpi=150)
    logger.info("Chart saved to %s", CHART_PATH)


    plt.show()
    plt.close()



def main():
    try:
        students = fetch_student_scores()
        df = calculate_averages(students)

        display_results(df)
        create_chart(df)

    except (requests.RequestException, ValueError) as exc:
        logger.error("Task failed: %s", exc)
        raise SystemExit(1)


if __name__ == "__main__":
    main()