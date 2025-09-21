from config.db import get_db

def add_student(student_data):
    db = get_db()
    students_collection = db["students"]
    return students_collection.insert_one(student_data)

def get_all_students():
    db = get_db()
    students_collection = db["students"]
    return list(students_collection.find({}, {"_id": 0}))
