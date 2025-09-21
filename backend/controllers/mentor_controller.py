from flask import jsonify, request
from models.mentor_model import add_mentor, get_all_mentors

def get_mentors():
    mentors = get_all_mentors()
    return jsonify(mentors)

def create_mentor():
    data = request.get_json()
    result = add_mentor(data)
    return jsonify({"message": "Mentor added", "id": str(result.inserted_id)})
