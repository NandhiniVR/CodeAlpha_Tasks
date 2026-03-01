#!/usr/bin/env python
"""Iris Flower Classification using Scikit-learn

This script demonstrates a simple machine‑learning workflow:
1. Load the Iris dataset from the CSV file you opened (Downloads/Iris (2).csv).
2. Split the data into training and test sets.
3. Train a Logistic Regression classifier (you can swap any estimator).
4. Evaluate accuracy on the held‑out test set.
5. Print a short classification report.

The code is heavily commented to help you understand each step.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
# The CSV you opened is located in your Downloads folder. Adjust the path if needed.
csv_path = os.path.expanduser(r"C:\Users\nandh\Downloads\Iris (2).csv")

# The file contains a header row with column names.
# We drop the "Id" column as it is not a feature.
df = pd.read_csv(csv_path)
X = df.drop(columns=["Id", "Species"]).values
y = df["Species"].values

# ---------------------------------------------------------------------------
# 2. Train‑test split
# ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------------------------------------------------------
# 3. Feature scaling (optional but improves many models)
# ---------------------------------------------------------------------------
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ---------------------------------------------------------------------------
# 4. Model training – Logistic Regression (multiclass "ovr" by default)
# ---------------------------------------------------------------------------
model = LogisticRegression(max_iter=200, solver="lbfgs", multi_class="auto")
model.fit(X_train, y_train)

# ---------------------------------------------------------------------------
# 5. Evaluation
# ---------------------------------------------------------------------------
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy on test set: {acc:.2%}")
print("\nClassification Report:\n", report)

# ---------------------------------------------------------------------------
# 6. Quick inference example (optional)
# ---------------------------------------------------------------------------
sample = [[5.1, 3.5, 1.4, 0.2]]  # typical setosa measurements
sample_scaled = scaler.transform(sample)
pred_species = model.predict(sample_scaled)[0]
print(f"Sample {sample[0]} predicted as: {pred_species}")

# End of script
