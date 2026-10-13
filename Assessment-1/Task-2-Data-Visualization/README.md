# Task 2: Student Score Analysis and Data Visualization

## Objective

Retrieve student test scores from a REST API, calculate the average score for each student, and visualize the results using a bar chart.

## Technologies Used

- Python - Programming language
- Flask - Local REST API
- Requests - HTTP requests
- Pandas - Data processing and average calculation
- Matplotlib - Data visualization

## Project Structure

```text
Task-2-Data-Visualization/
|-- student_scores.py
|-- student_scores_api.py
|-- requirements.txt
|-- README.md
`-- average_scores.png
```

## Implementation

### 1. API Data Retrieval

The `student_scores_api.py` script runs a local Flask API at the following endpoint:

`http://127.0.0.1:5000/api/student-scores`

The API returns student names and their test scores in JSON format.

**Note:** This project uses a locally created mock API with sample student data. It does not retrieve data from an external student-data service.

### 2. Average Score Calculation

The `student_scores.py` script sends an HTTP GET request to retrieve the JSON data. Pandas is used to process the scores and calculate the average for each student.

**Formula:**

Average score = Total of test scores / Number of tests

### 3. Data Visualization

Matplotlib generates a bar chart comparing the average scores of students. The chart is saved as `average_scores.png`.

## Sample Results

| Student | Test Scores | Average |
|---|---|---:|
| Rahul | 85, 90, 80 | 85.00 |
| Priya | 95, 92, 98 | 95.00 |
| Amit | 70, 75, 65 | 70.00 |
| Neha | 88, 84, 91 | 87.67 |

## How to Run

### Step 1: Install Dependencies

Open a terminal in the `Task-2-Data-Visualization` directory and run:

```bash
python -m pip install -r requirements.txt
```

### Step 2: Start the API

Open the first terminal and run:

```bash
python student_scores_api.py
```

Keep the API server running.

### Step 3: Run the Analysis

Open a second terminal in the same directory and run:

```bash
python student_scores.py
```

The script retrieves the data, calculates average scores, displays the results, and generates the chart.

## Error Handling

The implementation handles common issues such as API connection failures, HTTP errors, invalid JSON responses, and missing or invalid score data.

## Conclusion

This project demonstrates REST API communication, JSON processing, average calculation using Pandas, and data visualization with Matplotlib. It provides a basic example of a data analysis workflow using Python.