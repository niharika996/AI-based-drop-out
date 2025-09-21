from pymongo import MongoClient
import os

client = None
db = None

def init_db():
    global client, db
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    db = client["dropoutDB"]
    print("✅ MongoDB connected:", db.name)

def get_db():
    global db
    return db
