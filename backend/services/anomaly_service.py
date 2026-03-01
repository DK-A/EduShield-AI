import numpy as np
import joblib
import os

# Load model once at startup
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "anomaly_model.pkl")

model = joblib.load(MODEL_PATH)

def analyze_login(hour, device_known, location_match):
    input_data = np.array([[hour, device_known, location_match]])
    prediction = model.predict(input_data)[0]

    if prediction == -1:
        return {
            "risk": "High",
            "message": "Suspicious login detected",
            "reason": "Unusual time or unknown device/location"
        }
    else:
        return {
            "risk": "Low",
            "message": "Login appears normal"
        }