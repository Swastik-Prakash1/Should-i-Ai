from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import traceback
from trust_score import calculate_trust_score

app = Flask(__name__)
CORS(app)

# -------------------------------------------------
# Load trained model and vectorizer
# -------------------------------------------------
try:
    model = joblib.load("review_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    print("✅ Model and vectorizer loaded successfully.")
except Exception as e:
    print(f"[ERROR] Failed to load model/vectorizer: {e}")
    model = None
    vectorizer = None


# -------------------------------------------------
# Health check (useful for testing & deployment)
# -------------------------------------------------
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None
    })


# -------------------------------------------------
# Core analysis endpoint
# -------------------------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(force=True)

        reviews = data.get("reviews", [])
        rating = float(data.get("rating", 0))

        if model is None or vectorizer is None:
            return jsonify({"error": "Model not loaded"}), 500

        if not isinstance(reviews, list) or len(reviews) == 0:
            return jsonify({"error": "No reviews provided"}), 400

        # -----------------------------
        # Vectorize & predict
        # -----------------------------
        X = vectorizer.transform(reviews)
        predictions = model.predict(X)

        # -----------------------------
        # Count predictions
        # -----------------------------
        fake_count = 0
        genuine_count = 0

        for p in predictions:
            p_str = str(p).lower()
            if p_str in ["1", "fake", "f"]:
                fake_count += 1
            else:
                genuine_count += 1

        total_reviews = fake_count + genuine_count

        fake_percentage = round(
            (fake_count / total_reviews) * 100, 2
        ) if total_reviews > 0 else 0.0

        # -----------------------------
        # Trust score computation
        # -----------------------------
        trust_score = calculate_trust_score(
            fake_count=fake_count,
            genuine_count=genuine_count,
            rating=rating
        )

        # -----------------------------
        # Verdict logic (paper-friendly)
        # -----------------------------
        if fake_count > genuine_count:
            verdict = "Avoid buying — high proportion of suspicious reviews"
        elif fake_count == genuine_count:
            verdict = "Mixed signals — review authenticity is unclear"
        else:
            verdict = "Looks trustworthy based on review analysis"

        # -----------------------------
        # Response (used by extension + paper)
        # -----------------------------
        response = {
            "rating": rating,
            "total_reviews": total_reviews,
            "fake_count": fake_count,
            "genuine_count": genuine_count,
            "fake_percentage": fake_percentage,
            "trust_score": trust_score,
            "verdict": verdict
        }

        # Console log for qualitative evaluation
        print("\n[ANALYSIS RESULT]")
        print(f"Rating: {rating}")
        print(f"Total reviews: {total_reviews}")
        print(f"Fake reviews: {fake_count}")
        print(f"Genuine reviews: {genuine_count}")
        print(f"Fake %: {fake_percentage}%")
        print(f"Trust score: {trust_score}")
        print(f"Verdict: {verdict}")

        return jsonify(response), 200

    except Exception as e:
        print("❌ Error during analysis:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------
# Entry point
# -------------------------------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
