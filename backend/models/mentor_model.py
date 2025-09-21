from config.db import db

mentors_collection = db["mentors"]

def add_mentor(mentor_data):
    return mentors_collection.insert_one(mentor_data)

def get_all_mentors():
    return list(mentors_collection.find({}, {"_id": 0}))
