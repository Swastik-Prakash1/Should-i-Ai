import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_recall_curve,
    roc_curve,
    auc
)

# -----------------------------
# Load dataset
# -----------------------------
DATA_PATH = os.path.join("..", "data", "frd.csv")
df = pd.read_csv(DATA_PATH)

# Detect label column
label_col = None
for col in df.columns:
    if "label" in col.lower():
        label_col = col
        break

df = df.dropna(subset=[label_col, "text_"])
df["text_"] = df["text_"].astype(str)

df[label_col] = df[label_col].apply(
    lambda x: 1 if str(x).strip().lower() in ["fake", "cg", "spam", "fraud"] else 0
)

# -----------------------------
# Train-test split (same as training)
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    df["text_"],
    df[label_col],
    test_size=0.2,
    random_state=42,
    stratify=df[label_col]
)

# -----------------------------
# Load trained model & vectorizer
# -----------------------------
with open("review_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

X_test_vec = vectorizer.transform(X_test)

# Predictions
y_pred = model.predict(X_test_vec)
y_prob = model.predict_proba(X_test_vec)[:, 1]  # probability of FAKE

# =====================================================
# 1️⃣ CONFUSION MATRIX
# =====================================================
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Genuine", "Fake"],
    yticklabels=["Genuine", "Fake"]
)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix for Fake Review Detection")
plt.tight_layout()
plt.show()

# =====================================================
# 2️⃣ PRECISION–RECALL CURVE
# =====================================================
precision, recall, _ = precision_recall_curve(y_test, y_prob)

plt.figure(figsize=(6, 5))
plt.plot(recall, precision, linewidth=2)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision–Recall Curve (Fake Reviews)")
plt.grid(True)
plt.tight_layout()
plt.show()

# =====================================================
# 3️⃣ ROC CURVE + AUC
# =====================================================
fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve for Fake Review Detection")
plt.legend(loc="lower right")
plt.grid(True)
plt.tight_layout()
plt.show()

# =====================================================
# 4️⃣ ACCURACY COMPARISON (BAR CHART)
# =====================================================
# Update this value after retraining improved model
baseline_accuracy = 86.76
improved_accuracy = round((y_pred == y_test).mean() * 100, 2)

models = ["Baseline (Unigram)", "Improved (Uni + Bi)"]
accuracies = [baseline_accuracy, improved_accuracy]

plt.figure(figsize=(6, 4))
sns.barplot(x=models, y=accuracies)
plt.ylabel("Accuracy (%)")
plt.ylim(80, 100)
plt.title("Accuracy Comparison of Model Variants")
plt.tight_layout()
plt.show()
