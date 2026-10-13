# Task 2: Student Score Analysis and Data Visualization



## Objective



Retrieve student test scores from a REST API, calculate the average score for each student, and visualize the results using a bar chart.



## Technologies Used



\- Python

\- Flask â€” local REST API

\- Requests â€” HTTP requests

\- Pandas â€” data processing and average calculation

\- Matplotlib â€” data visualization



## Project Structure



```text

Task-2-Data-Visualization/

â”œâ”€â”€ student\_scores.py

â”œâ”€â”€ student\_scores\_api.py

â”œâ”€â”€ requirements.txt

â”œâ”€â”€ README.md

â””â”€â”€ average\_scores.png

```



## Implementation



### 1. API Data Retrieval



The `student\_scores\_api.py` script runs a local Flask API at:



`http://127.0.0.1:5000/api/student-scores`



The API returns student names and their test scores in JSON format.



\*\*Note:\*\* This project uses a locally created mock API and sample student data, not a real external student-data service.



### 2. Average Score Calculation



The `student\_scores.py` script sends an HTTP GET request to retrieve the JSON data. Pandas is used to organize the scores and calculate each student's average.



Average score = Total of test scores / Number of tests



### 3. Data Visualization



Matplotlib creates a bar chart comparing student average scores. The chart is saved as `average\_scores.png`.



## Sample Results



| Student | Test Scores | Average |

|---|---|---:|

| Rahul | 85, 90, 80 | 85.00 |

| Priya | 95, 92, 98 | 95.00 |

| Amit | 70, 75, 65 | 70.00 |

| Neha | 88, 84, 91 | 87.67 |



## How to Run



### Install Dependencies



Run these commands from this project directory:



```bash

python -m pip install -r requirements.txt

```



### Start the API



In the first terminal:



```bash

python student\_scores\_api.py

```



Keep the API server running.



### Run the Analysis



Open a second terminal in the same directory:



```bash

python student\_scores.py

```



The script retrieves the data, calculates average scores, displays the results, and generates the chart.



## Error Handling



The implementation accounts for common problems such as API connection failures, HTTP errors, invalid JSON responses, and missing or invalid score data.



## Conclusion



This project demonstrates REST API communication, JSON processing, average calculation with Pandas, and data visualization with Matplotlib. It provides a basic example of a data analysis workflow using Python.




