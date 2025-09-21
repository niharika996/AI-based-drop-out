from flask import jsonify, request
from models.subject_model import add_subject, get_all_subjects

def get_subjects():
    subjects = get_all_subjects()
    return jsonify(subjects)

def create_subject():
    data = request.get_json()
    result = add_subject(data)
    return jsonify({"message": "Subject added", "id": str(result.inserted_id)})
