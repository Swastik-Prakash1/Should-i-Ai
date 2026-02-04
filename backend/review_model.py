import pickle
import os

# Get the directory of this file (review_model.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model & vectorizer using absolute path
clf = pickle.load(open(os.path.join(BASE_DIR, "review_model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb"))

def analyze_reviews(data):
    reviews = data.get("reviews", [])
    if not reviews:
        return {"summary": {"verdict": "⚠️ No reviews to analyze"}}

    X = vectorizer.transform(reviews)
    preds = clf.predict(X)

    counts = {"Trusted":0, "Suspicious":0, "Fake":0}
    for p in preds:
        if p in counts:
            counts[p] += 1

    if counts["Fake"] > len(reviews)/2:
        verdict = "❌ Don’t Buy"
    elif counts["Suspicious"] > len(reviews)/2:
        verdict = "⚠️ Caution"
    else:
        verdict = "✅ Safe to Buy"

    return {"summary": {"verdict": verdict}, "counts": counts}
