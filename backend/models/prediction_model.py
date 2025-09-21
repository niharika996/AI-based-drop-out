from config.db import db

predictions_collection = db["predictions"]

def save_prediction(pred_data):
    return predictions_collection.insert_one(pred_data)

def get_all_predictions():
    return list(predictions_collection.find({}, {"_id": 0}))
