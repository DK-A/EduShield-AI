import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "phishing_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# =============================
# TRUSTED DOMAINS
# =============================
TRUSTED_DOMAINS = [
    "google.com",
    "gmail.com",
    "nptel.ac.in",
    "amd.com",
    "citchennai.net",
    "microsoft.com",
    "udemy.com"
]

SUSPICIOUS_KEYWORDS = [
    "urgent", "verify", "password",
    "click here", "account suspended",
    "limited time", "winner", "lottery"
]


# =============================
# DOMAIN ADJUSTMENT
# =============================
def adjust_score_for_domain(score, sender_email):

    if "@" not in sender_email:
        return score

    domain = sender_email.split("@")[1].lower()

    for trusted in TRUSTED_DOMAINS:
        if domain.endswith(trusted):
            score -= 30
            break

    return max(0, min(100, score))


# =============================
# SMART EXPLANATION
# =============================
def generate_explanation(score, sender_email, text):

    domain = sender_email.split("@")[-1] if "@" in sender_email else ""

    if score >= 75:
        summary = "High Risk Phishing Attempt"
    elif score >= 40:
        summary = "Suspicious Email Pattern"
    else:
        summary = "Low Risk Communication"

    reasons = []

    matched = [k for k in SUSPICIOUS_KEYWORDS if k in text.lower()]
    if matched:
        reasons.append(
            f"Detected suspicious keywords: {', '.join(matched)}"
        )

    if "http" in text.lower():
        reasons.append("Contains external hyperlink")

    if domain not in TRUSTED_DOMAINS:
        reasons.append("Sender domain not in trusted whitelist")
    else:
        reasons.append("Sender belongs to verified trusted domain")

    if not reasons:
        reasons.append("No malicious indicators detected")

    return {
        "summary": summary,
        "confidence": f"{score}%",
        "technical_reasons": reasons
    }


# =============================
# MAIN ANALYSIS FUNCTION
# =============================
def analyze_email(text: str, sender_email: str):

    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0][1]

    ml_score = prob * 100

    # Keyword boost
    keyword_hits = sum(word in text.lower() for word in SUSPICIOUS_KEYWORDS)
    rule_boost = keyword_hits * 5

    final_score = ml_score + rule_boost

    # Domain adjustment
    final_score = adjust_score_for_domain(final_score, sender_email)

    # Clamp
    final_score = max(0, min(100, int(final_score)))

    # Risk classification
    if final_score >= 75:
        risk_level = "High"
    elif final_score >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    explanation = generate_explanation(final_score, sender_email, text)

    return {
        "ml_probability": round(float(prob), 4),
        "final_risk_score": final_score,
        "risk_level": risk_level,
        "explanation": explanation
    }