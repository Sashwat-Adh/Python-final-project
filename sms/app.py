"""
app.py
------
This is the web server. It ties everything together:

  - Flask (a lightweight Python web framework) serves our HTML page and
    a JSON "API" that the browser's JavaScript talks to.
  - Every /api/... route reads or writes JSON files through DataManager.
  - We build/rebuild Student/Teacher/Course OBJECTS from the dicts we load
    (models.py) whenever we need their behaviour, then convert back to
    dicts with .to_dict() before sending JSON to the browser.

Run this file with:  python app.py
Then open:            http://127.0.0.1:5000 in your browser.
"""

import uuid
from datetime import date

from flask import Flask, jsonify, request, render_template

from data_manager import DataManager
from models import Student, Teacher, Course

app = Flask(__name__)

students_dm = DataManager("students.json")
teachers_dm = DataManager("teachers.json")
courses_dm = DataManager("courses.json")
marks_dm = DataManager("marks.json")
attendance_dm = DataManager("attendance.json")


# ---------------------------------------------------------------------------
# Page route
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------------------------------------------------------
# Students API
# ---------------------------------------------------------------------------

@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify(students_dm.load())


@app.route("/api/students", methods=["POST"])
def add_student():
    payload = request.get_json(force=True) or {}
    if not payload.get("name") or not payload.get("email"):
        return jsonify({"error": "name and email are required"}), 400

    student = Student(
        name=payload["name"],
        email=payload["email"],
        course_ids=payload.get("course_ids", []),
    )
    data = students_dm.load()
    data.append(student.to_dict())
    students_dm.save(data)
    return jsonify(student.to_dict()), 201


@app.route("/api/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    payload = request.get_json(force=True) or {}
    data = students_dm.load()
    for item in data:
        if item["id"] == student_id:
            item["name"] = payload.get("name", item["name"])
            item["email"] = payload.get("email", item["email"])
            item["course_ids"] = payload.get("course_ids", item.get("course_ids", []))
            students_dm.save(data)
            return jsonify(item)
    return jsonify({"error": "student not found"}), 404


@app.route("/api/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    data = students_dm.load()
    new_data = [s for s in data if s["id"] != student_id]
    if len(new_data) == len(data):
        return jsonify({"error": "student not found"}), 404
    students_dm.save(new_data)
    return jsonify({"deleted": student_id})


# ---------------------------------------------------------------------------
# Teachers API
# ---------------------------------------------------------------------------

@app.route("/api/teachers", methods=["GET"])
def get_teachers():
    return jsonify(teachers_dm.load())


@app.route("/api/teachers", methods=["POST"])
def add_teacher():
    payload = request.get_json(force=True) or {}
    if not payload.get("name") or not payload.get("email"):
        return jsonify({"error": "name and email are required"}), 400

    teacher = Teacher(
        name=payload["name"],
        email=payload["email"],
        subject=payload.get("subject", ""),
    )
    data = teachers_dm.load()
    data.append(teacher.to_dict())
    teachers_dm.save(data)
    return jsonify(teacher.to_dict()), 201


@app.route("/api/teachers/<teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    data = teachers_dm.load()
    new_data = [t for t in data if t["id"] != teacher_id]
    if len(new_data) == len(data):
        return jsonify({"error": "teacher not found"}), 404
    teachers_dm.save(new_data)
    return jsonify({"deleted": teacher_id})


# ---------------------------------------------------------------------------
# Courses API
# ---------------------------------------------------------------------------

@app.route("/api/courses", methods=["GET"])
def get_courses():
    return jsonify(courses_dm.load())


@app.route("/api/courses", methods=["POST"])
def add_course():
    payload = request.get_json(force=True) or {}
    if not payload.get("name") or not payload.get("code"):
        return jsonify({"error": "name and code are required"}), 400

    course = Course(
        name=payload["name"],
        code=payload["code"],
        teacher_id=payload.get("teacher_id"),
        credits=payload.get("credits", 3),
    )
    data = courses_dm.load()
    data.append(course.to_dict())
    courses_dm.save(data)
    return jsonify(course.to_dict()), 201


@app.route("/api/courses/<course_id>", methods=["DELETE"])
def delete_course(course_id):
    data = courses_dm.load()
    new_data = [c for c in data if c["id"] != course_id]
    if len(new_data) == len(data):
        return jsonify({"error": "course not found"}), 404
    courses_dm.save(new_data)
    return jsonify({"deleted": course_id})


# ---------------------------------------------------------------------------
# Marks API
# ---------------------------------------------------------------------------

@app.route("/api/marks", methods=["GET"])
def get_marks():
    return jsonify(marks_dm.load())


@app.route("/api/marks", methods=["POST"])
def add_mark():
    payload = request.get_json(force=True) or {}
    required = ("student_id", "course_id", "score", "max_score")
    if not all(k in payload for k in required):
        return jsonify({"error": f"required fields: {', '.join(required)}"}), 400

    entry = {
        "id": str(uuid.uuid4())[:8],
        "student_id": payload["student_id"],
        "course_id": payload["course_id"],
        "score": float(payload["score"]),
        "max_score": float(payload["max_score"]),
        "date": payload.get("date", str(date.today())),
    }
    data = marks_dm.load()
    data.append(entry)
    marks_dm.save(data)
    return jsonify(entry), 201


@app.route("/api/marks/<mark_id>", methods=["DELETE"])
def delete_mark(mark_id):
    data = marks_dm.load()
    new_data = [m for m in data if m["id"] != mark_id]
    if len(new_data) == len(data):
        return jsonify({"error": "mark not found"}), 404
    marks_dm.save(new_data)
    return jsonify({"deleted": mark_id})


# ---------------------------------------------------------------------------
# Attendance API
# ---------------------------------------------------------------------------

@app.route("/api/attendance", methods=["GET"])
def get_attendance():
    return jsonify(attendance_dm.load())


@app.route("/api/attendance", methods=["POST"])
def add_attendance():
    payload = request.get_json(force=True) or {}
    required = ("student_id", "course_id", "status")
    if not all(k in payload for k in required):
        return jsonify({"error": f"required fields: {', '.join(required)}"}), 400

    if payload["status"] not in ("Present", "Absent", "Late"):
        return jsonify({"error": "status must be Present, Absent or Late"}), 400

    entry = {
        "id": str(uuid.uuid4())[:8],
        "student_id": payload["student_id"],
        "course_id": payload["course_id"],
        "status": payload["status"],
        "date": payload.get("date", str(date.today())),
    }
    data = attendance_dm.load()
    data.append(entry)
    attendance_dm.save(data)
    return jsonify(entry), 201


@app.route("/api/attendance/<record_id>", methods=["DELETE"])
def delete_attendance(record_id):
    data = attendance_dm.load()
    new_data = [a for a in data if a["id"] != record_id]
    if len(new_data) == len(data):
        return jsonify({"error": "record not found"}), 404
    attendance_dm.save(new_data)
    return jsonify({"deleted": record_id})


# ---------------------------------------------------------------------------
# Statistics API  (Week 3 collections + a bit of arithmetic)
# ---------------------------------------------------------------------------

@app.route("/api/statistics", methods=["GET"])
def get_statistics():
    students = students_dm.load()
    teachers = teachers_dm.load()
    courses = courses_dm.load()
    marks = marks_dm.load()
    attendance = attendance_dm.load()

    # Average mark as a percentage, across all recorded marks
    if marks:
        percentages = [(m["score"] / m["max_score"]) * 100 for m in marks if m["max_score"]]
        avg_mark = round(sum(percentages) / len(percentages), 2) if percentages else 0
    else:
        avg_mark = 0

    # Attendance rate: % of records marked "Present"
    if attendance:
        present_count = sum(1 for a in attendance if a["status"] == "Present")
        attendance_rate = round((present_count / len(attendance)) * 100, 2)
    else:
        attendance_rate = 0

    # Top student by average mark
    top_student = None
    if marks and students:
        by_student = {}
        for m in marks:
            by_student.setdefault(m["student_id"], []).append((m["score"] / m["max_score"]) * 100)
        averages = {sid: sum(v) / len(v) for sid, v in by_student.items()}
        if averages:
            top_id = max(averages, key=averages.get)
            match = next((s for s in students if s["id"] == top_id), None)
            if match:
                top_student = {"name": match["name"], "average": round(averages[top_id], 2)}

    return jsonify({
        "total_students": len(students),
        "total_teachers": len(teachers),
        "total_courses": len(courses),
        "total_marks_recorded": len(marks),
        "average_mark_percent": avg_mark,
        "attendance_rate_percent": attendance_rate,
        "top_student": top_student,
    })


if __name__ == "__main__":
    app.run(debug=True)
