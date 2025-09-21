from flask import Blueprint
from controllers.subject_controller import get_subjects, create_subject

subject_bp = Blueprint("subject_bp", __name__)

@subject_bp.route("/", methods=["GET"])
def fetch_subjects():
    return get_subjects()

@subject_bp.route("/", methods=["POST"])
def add_new_subject():
    return create_subject()
