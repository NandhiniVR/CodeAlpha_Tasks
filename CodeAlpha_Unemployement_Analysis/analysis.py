import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configure seaborn style for premium visuals
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({
    "figure.figsize": (12, 6),
    "axes.titlesize": 16,
    "axes.labelsize": 14,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})

# Paths
DATA_PATH = r"d:\\Unemployement-Ratio\\Unemployment in India.csv"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
# The CSV uses commas as separators and may contain extra whitespace
df = pd.read_csv(DATA_PATH)

# Basic cleaning
# Strip whitespace from column names
df.columns = df.columns.str.strip()
# Ensure proper column names (handle possible variations)
expected_cols = ["Region", "Date", "Frequency", "Estimated Unemployment Rate (%)", "Estimated Employed", "Estimated Labour Participation Rate (%)", "Area"]
# Rename columns to standardized names if needed
col_map = {col: std for col, std in zip(df.columns, expected_cols)}
df = df.rename(columns=col_map)
# Parse dates (format like DD-MM-YYYY)
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
# Drop rows with invalid dates
df = df.dropna(subset=["Date"])
# Convert unemployment rate to numeric (handle commas, missing)
df["UnemploymentRate"] = pd.to_numeric(df["Estimated Unemployment Rate (%)"], errors="coerce")
# Drop rows where rate is missing
df = df.dropna(subset=["UnemploymentRate"])
# Add Year and Month columns for seasonal analysis
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month

# 1. Overall national trend (average across regions)
national_trend = df.groupby("Date")["UnemploymentRate"].mean().reset_index()
plt.figure()
plt.plot(national_trend["Date"], national_trend["UnemploymentRate"], marker="o", linestyle="-")
plt.title("National Average Unemployment Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "national_trend.png"))
plt.close()

# 2. Covid‑19 impact (compare 2019 vs 2020)
pre_covid = df[df["Year"] < 2020]
post_covid = df[df["Year"] >= 2020]
pre_avg = pre_covid.groupby("Month")["UnemploymentRate"].mean()
post_avg = post_covid.groupby("Month")["UnemploymentRate"].mean()
plt.figure()
months = range(1, 13)
plt.plot(months, pre_avg.reindex(months), label="2019 (Pre‑COVID)", marker="o")
plt.plot(months, post_avg.reindex(months), label="2020 (COVID)", marker="o")
plt.title("Monthly Unemployment Rate: Pre vs During COVID‑19")
plt.xlabel("Month")
plt.ylabel("Unemployment Rate (%)")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "covid_impact.png"))
plt.close()

# 3. Seasonal pattern (average across all years)
seasonal = df.groupby("Month")["UnemploymentRate"].mean()
plt.figure()
plt.plot(seasonal.index, seasonal.values, marker="o")
plt.title("Average Seasonal Unemployment Rate (All Years)")
plt.xlabel("Month")
plt.ylabel("Unemployment Rate (%)")
plt.xticks(months)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "seasonal_trend.png"))
plt.close()

# 4. Region‑wise heatmap for 2020
region_2020 = df[df["Year"] == 2020]
pivot = region_2020.pivot_table(values="UnemploymentRate", index="Region", columns="Month", aggfunc="mean")
plt.figure(figsize=(14, 10))
sns.heatmap(pivot, cmap="YlOrRd", linewidths=.5, annot=True, fmt=".1f")
plt.title("Unemployment Rate by Region (2020)")
plt.xlabel("Month")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "region_heatmap_2020.png"))
plt.close()

print("Analysis complete. Plots saved to:")
for f in os.listdir(OUTPUT_DIR):
    print(os.path.join(OUTPUT_DIR, f))
