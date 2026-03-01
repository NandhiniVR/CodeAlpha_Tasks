import os
import csv
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

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

# Helper to parse a row
# Expected columns: Region, Date, Frequency, Estimated Unemployment Rate (%), Estimated Employed, Estimated Labour Participation Rate (%), Area
def parse_row(row):
    try:
        region = row[0].strip()
        date_str = row[1].strip()
        date = datetime.strptime(date_str, "%d-%m-%Y")
        unemployment_rate = float(row[3].strip()) if row[3].strip() else None
        return {"Region": region, "Date": date, "UnemploymentRate": unemployment_rate}
    except Exception:
        return None

# Load data
records = []
with open(DATA_PATH, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # skip header
    for row in reader:
        if not row or len(row) < 4:
            continue
        parsed = parse_row(row)
        if parsed and parsed["UnemploymentRate"] is not None:
            records.append(parsed)

# Aggregate national average per date
national_by_date = {}
for rec in records:
    d = rec["Date"]
    national_by_date.setdefault(d, []).append(rec["UnemploymentRate"])

national_dates = sorted(national_by_date.keys())
national_avg = [sum(vals) / len(vals) for vals in (national_by_date[d] for d in national_dates)]

plt.figure()
plt.plot(national_dates, national_avg, marker="o", linestyle="-")
plt.title("National Average Unemployment Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "national_trend.png"))
plt.close()

# Covid impact: compare 2019 vs 2020 monthly averages
monthly_pre = {}
monthly_post = {}
for rec in records:
    year = rec["Date"].year
    month = rec["Date"].month
    if year < 2020:
        monthly_pre.setdefault(month, []).append(rec["UnemploymentRate"])
    else:
        monthly_post.setdefault(month, []).append(rec["UnemploymentRate"])

months = range(1, 13)
pre_avg = [np.mean(monthly_pre[m]) if monthly_pre.get(m) else np.nan for m in months]
post_avg = [np.mean(monthly_post[m]) if monthly_post.get(m) else np.nan for m in months]

plt.figure()
plt.plot(months, pre_avg, label="2019 (Pre‑COVID)", marker="o")
plt.plot(months, post_avg, label="2020 (COVID)", marker="o")
plt.title("Monthly Unemployment Rate: Pre vs During COVID‑19")
plt.xlabel("Month")
plt.ylabel("Unemployment Rate (%)")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "covid_impact.png"))
plt.close()

# Seasonal pattern across all years
monthly_all = {}
for rec in records:
    month = rec["Date"].month
    monthly_all.setdefault(month, []).append(rec["UnemploymentRate"])
seasonal_avg = [np.mean(monthly_all[m]) if monthly_all.get(m) else np.nan for m in months]

plt.figure()
plt.plot(months, seasonal_avg, marker="o")
plt.title("Average Seasonal Unemployment Rate (All Years)")
plt.xlabel("Month")
plt.ylabel("Unemployment Rate (%)")
plt.xticks(months)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "seasonal_trend.png"))
plt.close()

# Region‑wise heatmap for 2020
region_month = {}
for rec in records:
    if rec["Date"].year == 2020:
        region = rec["Region"]
        month = rec["Date"].month
        region_month.setdefault(region, {}).setdefault(month, []).append(rec["UnemploymentRate"])

regions = sorted(region_month.keys())
heatmap_matrix = []
for region in regions:
    row = []
    for m in months:
        vals = region_month[region].get(m, [])
        row.append(np.mean(vals) if vals else np.nan)
    heatmap_matrix.append(row)

heatmap_array = np.array(heatmap_matrix, dtype=float)
plt.figure(figsize=(14, 10))
sns.heatmap(heatmap_array, cmap="YlOrRd", linewidths=.5, annot=True, fmt=".1f",
            yticklabels=regions, xticklabels=months)
plt.title("Unemployment Rate by Region (2020)")
plt.xlabel("Month")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "region_heatmap_2020.png"))
plt.close()

print("Analysis complete. Plots saved to:")
for f in os.listdir(OUTPUT_DIR):
    print(os.path.join(OUTPUT_DIR, f))
