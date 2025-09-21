from flask import Flask
from config.db import init_db
from routes.student_routes import student_bp
from routes.mentor_routes import mentor_bp
from routes.subject_routes import subject_bp
from routes.prediction_routes import prediction_bp

app = Flask(__name__)

# Init DB
init_db()

# Register Blueprints
app.register_blueprint(student_bp, url_prefix="/api/students")
app.register_blueprint(mentor_bp, url_prefix="/api/mentors")
app.register_blueprint(subject_bp, url_prefix="/api/subjects")
app.register_blueprint(prediction_bp, url_prefix="/api/predictions")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
