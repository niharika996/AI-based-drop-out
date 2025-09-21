from flask import Blueprint
from controllers.mentor_controller import get_mentors, create_mentor

mentor_bp = Blueprint("mentor_bp", __name__)

@mentor_bp.route("/", methods=["GET"])
def fetch_mentors():
    return get_mentors()

@mentor_bp.route("/", methods=["POST"])
def add_new_mentor():
    return create_mentor()
