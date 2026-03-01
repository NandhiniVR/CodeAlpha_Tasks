#!/usr/bin/env python
"""
Visualization script for the Iris classification project.

- Generates a pair‑plot of the four features colored by species.
- Trains the same Logistic Regression model as `train_iris.py` (for reproducibility).
- Plots a confusion matrix heat‑map.
- Saves all figures into a `plots/` directory.

Run with:
    python visualize_iris.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
csv_path = os.path.expanduser(r"C:\\Users\\nandh\\Downloads\\Iris (2).csv")
df = pd.read_csv(csv_path)
X = df.drop(columns=["Id", "Species"]).values
y = df["Species"].values

# ---------------------------------------------------------------------------
# 2. Visualise data – pair plot
# ---------------------------------------------------------------------------
sns.set(style="whitegrid", palette="muted")
pair_plot = sns.pairplot(df, hue="Species", vars=["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"], corner=True)
# Ensure output directory exists
os.makedirs("plots", exist_ok=True)
pair_plot_path = os.path.join("plots", "pairplot.png")
pair_plot.savefig(pair_plot_path)
plt.close()

# ---------------------------------------------------------------------------
# 3. Train‑test split & model (same as train_iris.py)
# ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
model = LogisticRegression(max_iter=200, solver="lbfgs", multi_class="auto")
model.fit(X_train, y_train)

# ---------------------------------------------------------------------------
# 4. Confusion matrix heat‑map
# ---------------------------------------------------------------------------
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=model.classes_, yticklabels=model.classes_, ax=ax)
ax.set_xlabel("Predicted")
ax.set_ylabel("True")
ax.set_title("Confusion Matrix")
conf_mat_path = os.path.join("plots", "confusion_matrix.png")
fig.savefig(conf_mat_path)
plt.close()

print("Plots saved to the 'plots/' directory:")
print(f"  - {pair_plot_path}")
print(f"  - {conf_mat_path}")
