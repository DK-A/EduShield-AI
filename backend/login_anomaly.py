import numpy as np
from sklearn.ensemble import IsolationForest

# Simulated normal login data
# Features: [hour_of_day, device_known(0/1), location_match(0/1)]
normal_data = np.array([
    [9, 1, 1],
    [10, 1, 1],
    [11, 1, 1],
    [20, 1, 1],
    [21, 1, 1],
    [8, 1, 1],
    [19, 1, 1]
])

model = IsolationForest(contamination=0.2)
model.fit(normal_data)

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