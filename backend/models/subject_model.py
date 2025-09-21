from config.db import db

subjects_collection = db["subjects"]

def add_subject(subject_data):
    return subjects_collection.insert_one(subject_data)

def get_all_subjects():
    return list(subjects_collection.find({}, {"_id": 0}))
