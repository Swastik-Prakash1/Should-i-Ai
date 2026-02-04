import pandas as pd
import os
import re
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# -------------------------------------------------
# Dataset path
# -------------------------------------------------
DATA_PATH = os.path.join("..", "data", "frd.csv")

print("[INFO] Loading dataset...")
df = pd.read_csv(DATA_PATH)
print("[INFO] Columns:", df.columns)

# -------------------------------------------------
# Detect label column
# -------------------------------------------------
label_col = None
for col in df.columns:
    if "label" in col.lower():
        label_col = col
        break

if label_col is None:
    raise ValueError("No label column found in dataset!")

# -------------------------------------------------
# Basic cleaning (lightweight, safe)
# -------------------------------------------------
df = df.dropna(subset=[label_col, "text_"])
df["text_"] = df["text_"].astype(str)

# Normalize text
df["text_"] = df["text_"].str.lower()

# Remove excessive character repetition (e.g., goooood → good)
df["text_"] = df["text_"].apply(
    lambda x: re.sub(r"(.)\1{2,}", r"\1\1", x)
)

# Binary labels: 1 = fake, 0 = genuine
df[label_col] = df[label_col].apply(
    lambda x: 1 if str(x).strip().lower() in ["fake", "cg", "spam", "fraud"] else 0
)

print("[INFO] Dataset size:", len(df))
print("[INFO] Fake reviews:", df[label_col].sum())
print("[INFO] Genuine reviews:", len(df) - df[label_col].sum())

# -------------------------------------------------
# Train-test split
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    df["text_"],
    df[label_col],
    test_size=0.2,
    random_state=42,
    stratify=df[label_col]
)

# -------------------------------------------------
# TF-IDF with bi-grams (MAIN IMPROVEMENT)
# -------------------------------------------------
print("[INFO] Vectorizing text (unigrams + bigrams)...")

vectorizer = TfidfVectorizer(
    max_features=15000,
    stop_words="english",
    ngram_range=(1, 2)
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# -------------------------------------------------
# Logistic Regression (stable, interpretable)
# -------------------------------------------------
print("[INFO] Training Logistic Regression model...")

model = LogisticRegression(
    max_iter=2000,
    solver="liblinear",
    class_weight="balanced",
    C=2.0
)

model.fit(X_train_vec, y_train)

# -------------------------------------------------
# Evaluation
# -------------------------------------------------
y_pred = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n[RESULT] Model Accuracy: {accuracy * 100:.2f}%\n")

print("[RESULT] Classification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Genuine", "Fake"]
))

# -------------------------------------------------
# Save artifacts
# -------------------------------------------------
with open("review_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("[INFO] Model and vectorizer saved successfully!")
