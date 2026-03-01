import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import joblib
import os

# CHANGE filename here
df = pd.read_csv("data_set.csv")

# IMPORTANT: Adjust column names if needed
# Based on your screenshot, likely:

df = df.dropna()

X_text = df.iloc[:, 0]   # First column = email text
y = df.iloc[:, 1]        # Second column = label (0/1)

vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(X_text)

model = XGBClassifier(eval_metric="logloss")
model.fit(X, y)

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/phishing_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("Kaggle model trained successfully!")