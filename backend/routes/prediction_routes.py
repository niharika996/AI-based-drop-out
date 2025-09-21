from flask import Blueprint
from controllers.prediction_controller import train, predict

prediction_bp = Blueprint("prediction_bp", __name__)

@prediction_bp.route("/train", methods=["POST"])
def train_route():
    return train()

@prediction_bp.route("/predict", methods=["POST"])
def predict_route():
    return predict()
