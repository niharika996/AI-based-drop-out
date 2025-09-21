import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

from utils.thresholds import thresholds
from config.db import db

predictions_collection = db["predictions"]

# --- Helper: Convert numeric values into R/O/G ---
def apply_thresholds(row):
    def classify(value, rules, reverse=False):
        if "red" in rules:
            if reverse:  # attempts & fees (higher = risky)
                if value > rules["red"]:
                    return "R"
            else:  # attendance & marks (lower = risky)
                if value < rules["red"]:
                    return "R"
        if "orange" in rules:
            low, high = rules["orange"]
            if low <= value <= high:
                return "O"
        return "G"

    return {
        "attendance": classify(row["attendance"], thresholds["attendance"]),
        "marks": classify(row["marks"], thresholds["marks"]),
        "attempts": classify(row["attempts"], thresholds["attempts"], reverse=True),
        "fees": classify(row["fees"], thresholds["fees"], reverse=True),
    }

# --- Label Rules ---
def assign_label(row):
    if row["attendance"] == "R" or row["fees"] == "R":
        return "R"
    if row["marks"] == "R" and row["attempts"] == "R":
        return "R"
    if row["attendance"] == "O" or row["fees"] == "O":
        return "O"
    if row["marks"] == "O" and row["attempts"] == "O":
        return "O"
    return "G"

# --- Train Model ---
def train_model(merged_csv_path="data/merged_dataset.csv", model_path="dropout_model.pkl"):
    df = pd.read_csv(merged_csv_path)

    classified = df.apply(apply_thresholds, axis=1, result_type="expand")
    df = pd.concat([df, classified], axis=1)
    df["label"] = df.apply(assign_label, axis=1)

    mapping = {"R": 0, "O": 1, "G": 2}
    X = df[["attendance", "marks", "attempts", "fees"]].replace(mapping)
    y = df["label"].replace(mapping)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    acc = model.score(X_test, y_test)
    return {"accuracy": acc, "message": "Model trained successfully"}

# --- Predict ---
def predict_dropout(student_data, model_path="dropout_model.pkl"):
    if not os.path.exists(model_path):
        return {"error": "Model not trained yet"}

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    classified = apply_thresholds(student_data)
    features = [[
        {"R": 0, "O": 1, "G": 2}[classified["attendance"]],
        {"R": 0, "O": 1, "G": 2}[classified["marks"]],
        {"R": 0, "O": 1, "G": 2}[classified["attempts"]],
        {"R": 0, "O": 1, "G": 2}[classified["fees"]],
    ]]

    prediction = model.predict(features)[0]
    label = {0: "R", 1: "O", 2: "G"}[prediction]

    predictions_collection.insert_one({
        "student_id": student_data.get("rollNo", "unknown"),
        "classified": classified,
        "prediction": label
    })

    return {"prediction": label, "classified": classified}
