from flask import Flask, jsonify

app = Flask(__name__)


STUDENTS = [
    {
        "name": "Rahul",
        "scores": {
            "Mathematics": 85,
            "Science": 90,
            "English": 80
        }
    },
    {
        "name": "Priya",
        "scores": {
            "Mathematics": 95,
            "Science": 92,
            "English": 98
        }
    },
    {
        "name": "Amit",
        "scores": {
            "Mathematics": 70,
            "Science": 75,
            "English": 65
        }
    },
    {
        "name": "Neha",
        "scores": {
            "Mathematics": 88,
            "Science": 84,
            "English": 91
        }
    }
]


@app.get("/api/student-scores")
def get_student_scores():
    return jsonify({"students": STUDENTS})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)