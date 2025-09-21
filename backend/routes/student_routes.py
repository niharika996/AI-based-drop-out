from flask import Blueprint
from controllers.student_controller import get_students, create_student

student_bp = Blueprint("student_bp", __name__)

@student_bp.route("/", methods=["GET"])
def fetch_students():
    return get_students()

@student_bp.route("/", methods=["POST"])
def add_new_student():
    return create_student()
