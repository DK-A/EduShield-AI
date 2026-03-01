import numpy as np
import joblib
from sklearn.ensemble import IsolationForest

normal_data = np.array([
    [9, 1, 1],
    [10, 1, 1],
    [11, 1, 1],
    [20, 1, 1],
    [21, 1, 1],
    [8, 1, 1],
    [19, 1, 1]
])

model = IsolationForest(contamination=0.2, random_state=42)
model.fit(normal_data)

joblib.dump(model, "anomaly_model.pkl")

print("Anomaly model saved!")