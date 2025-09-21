from flask import jsonify, request
from services.ml_service import train_model, predict_dropout
from services.csv_service import merge_csvs

def train():
    # Merge CSV files into merged_dataset.csv before training
    merge_csvs([
        "data/attendance.csv",
        "data/marks.csv",
        "data/attempts.csv",
        "data/fees.csv"
    ])
    result = train_model("data/merged_dataset.csv")
    return jsonify(result)

def predict():
    data = request.get_json()
    result = predict_dropout(data)
    return jsonify(result)
