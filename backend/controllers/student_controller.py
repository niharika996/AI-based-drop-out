from flask import jsonify, request
from models.student_model import add_student, get_all_students

def get_students():
    students = get_all_students()
    return jsonify(students)

def create_student():
    data = request.get_json()
    result = add_student(data)
    return jsonify({"message": "Student added", "id": str(result.inserted_id)})
