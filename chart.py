import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Generate synthetic seasonal revenue data
np.random.seed(2025)
months = pd.date_range(start="2022-01-01", periods=24, freq='MS')
regions = ["North America", "Europe", "Asia Pacific"]
data = []
for region in regions:
    base = {"North America": 500, "Europe": 350, "Asia Pacific": 300}[region]
    trend = np.linspace(0, 80, len(months))
    seasonal = 50 * np.sin(2 * np.pi * (np.arange(len(months)) % 12) / 12)
    noise = np.random.normal(scale=20, size=len(months))
    revenue = base + trend + seasonal + noise
    for dt, rev in zip(months, revenue):
        data.append({"date": dt, "region": region, "revenue": round(rev, 2)})

df = pd.DataFrame(data)

sns.set_style("whitegrid")
sns.set_context("talk", font_scale=0.9)

plt.figure(figsize=(8,8))
palette = sns.color_palette("tab10", n_colors=len(regions))
ax = sns.lineplot(data=df, x="date", y="revenue", hue="region", palette=palette,
                  marker="o", linewidth=2.2, markersize=6)

ax.set_title("Seasonal Revenue by Region (Monthly) — 2-Year Period", fontsize=16, weight='bold')
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Revenue (USD thousands)", fontsize=12)
ax.xaxis.set_major_locator(plt.MaxNLocator(8))
plt.xticks(rotation=45, ha='right')

avg_by_month = df.groupby(df['date'].dt.to_period('M'))['revenue'].mean()
peak_month = avg_by_month.idxmax().to_timestamp()
peak_value = avg_by_month.max()

ax.axvline(peak_month, color='gray', linestyle='--', linewidth=1)
ax.text(peak_month, peak_value + 30, f"Peak Avg: {peak_month.strftime('%Y-%m')}", 
        rotation=90, va='bottom', ha='center', fontsize=10, color='gray')

plt.legend(title="Region", loc="upper left")
plt.tight_layout()
plt.savefig("chart.png", dpi=64, bbox_inches='tight')
plt.close()
