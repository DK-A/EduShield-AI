import joblib
import numpy as np

model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

def analyze_email(text):
    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0][1]

    label = "phishing" if prob > 0.5 else "legitimate"

    explanation = []

    # Simple keyword reasoning (for demo clarity)
    keywords = {
        "urgent": "Uses urgency language",
        "password": "Requests password information",
        "verify": "Asks for account verification",
        "click": "Contains clickable instruction",
        "account": "Mentions account action",
        "bank": "Mentions financial details",
        "2fa": "Requests two-factor authentication code"
    }

    for word, reason in keywords.items():
        if word in text.lower():
            explanation.append(reason)

    if len(explanation) == 0:
        explanation.append("No obvious phishing indicators detected")

    return {
        "risk_score": round(float(prob), 2),
        "label": label,
        "risk_level": (
            "High" if prob > 0.75
            else "Medium" if prob > 0.5
            else "Low"
        ),
        "explanation": explanation
    }