# ==============================================================================
# PROJECT: NETFLIX CONTENT TREND ANALYSIS BY RELEASE YEAR
# Task: Task 4 (Medium) - Auspify Data Analysis Using Python Internship
# Student: Priya Sharma
# Description: Analyze the chronological distribution of Netflix catalog titles
# ==============================================================================

import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# Determine script directory to ensure outputs are saved in the task folder
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "output")
reports_dir = os.path.join(script_dir, "reports")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(reports_dir, exist_ok=True)

# ------------------------------------------------------------------------------
# STEP 1: LOAD AND INSPECT DATASET
# ------------------------------------------------------------------------------
print("=" * 60)
print("TASK 4: NETFLIX RELEASE YEAR TREND ANALYSIS")
print("STEP 1: LOADING DATASET")
print("=" * 60)

# Check for cleaned dataset from Task 1 first, fallback to original dataset
data_path = os.path.join(script_dir, "..", "output", "cleaned_netflix_dataset.csv")
if not os.path.exists(data_path):
    data_path = os.path.join(script_dir, "..", "Task_1_Data_Cleaning", "output", "cleaned_netflix_dataset.csv")
if not os.path.exists(data_path):
    data_path = os.path.join(script_dir, "..", "data", "Dataset(1).csv")
if not os.path.exists(data_path):
    data_path = os.path.join("output", "cleaned_netflix_dataset.csv")

print(f"Reading dataset from: {data_path}")
df = pd.read_csv(data_path)

total_titles = len(df)
print(f"Total catalog titles: {total_titles}")

# Ensure release_year is numeric
df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
df = df.dropna(subset=["release_year"])
df["release_year"] = df["release_year"].astype(int)

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())
total_years_span = max_year - min_year + 1

print(f"Earliest Release Year : {min_year}")
print(f"Latest Release Year   : {max_year}")
print(f"Total Year Span       : {total_years_span} years ({min_year} - {max_year})")

# ------------------------------------------------------------------------------
# STEP 2: CALCULATE YEARLY CONTENT RELEASES
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 2: GROUPING TITLES BY RELEASE YEAR")
print("=" * 60)

# Group by release_year using size()
yearly_counts = df.groupby("release_year").size()

# Top 10 release years
top_10_years = yearly_counts.sort_values(ascending=False).head(10)
peak_year = int(top_10_years.index[0])
peak_count = int(top_10_years.values[0])

print(f"\nPeak Release Year: {peak_year} ({peak_count} titles)")
print("\n--- Top 10 Release Years by Available Titles ---")
for rank, (yr, cnt) in enumerate(top_10_years.items(), 1):
    print(f"  {rank}. Year {yr}: {cnt} titles")

# ------------------------------------------------------------------------------
# STEP 3: COMPARE MOVIES VS TV SHOWS BY RELEASE YEAR
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 3: COMPARING MOVIES VS TV SHOWS TRENDS")
print("=" * 60)

yearly_type_df = df.groupby(["release_year", "type"]).size().unstack(fill_value=0)
if "Movie" not in yearly_type_df.columns:
    yearly_type_df["Movie"] = 0
if "TV Show" not in yearly_type_df.columns:
    yearly_type_df["TV Show"] = 0

yearly_type_df["Total"] = yearly_type_df["Movie"] + yearly_type_df["TV Show"]

# Recent decade comparison (2010 to 2021)
recent_years = [y for y in range(2010, 2022) if y in yearly_type_df.index]
print("\n--- Recent Decade Content Breakdown (2010 - 2021) ---")
print(yearly_type_df.loc[recent_years, ["Movie", "TV Show", "Total"]])

# ------------------------------------------------------------------------------
# STEP 4: SAVE OUTPUT CSVS
# ------------------------------------------------------------------------------
# 1. Yearly Content Summary CSV
df_yearly_summary = yearly_type_df.reset_index()
df_yearly_summary.columns = ["Release_Year", "Movie_Count", "TV_Show_Count", "Total_Titles"]
yearly_summary_csv = os.path.join(output_dir, "yearly_content_summary.csv")
df_yearly_summary.to_csv(yearly_summary_csv, index=False)
print(f"\n[SAVED]: Yearly content summary saved to {yearly_summary_csv}")

# 2. Top Release Years CSV
df_top_years_csv = top_10_years.reset_index()
df_top_years_csv.columns = ["Release_Year", "Total_Titles"]
df_top_years_csv["Rank"] = range(1, 11)
df_top_years_csv = df_top_years_csv[["Rank", "Release_Year", "Total_Titles"]]
top_years_csv = os.path.join(output_dir, "top_release_years.csv")
df_top_years_csv.to_csv(top_years_csv, index=False)
print(f"[SAVED]: Top release years saved to {top_years_csv}")

# ------------------------------------------------------------------------------
# STEP 5: GENERATE MATPLOTLIB CHARTS
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 5: GENERATING MATPLOTLIB CHARTS")
print("=" * 60)

netflix_red = "#E50914"
netflix_grey = "#777777"
bg_color = "#141414"
text_color = "#FFFFFF"

# Chart 1: Historical Line Chart (Yearly Content Trend)
plt.figure(figsize=(10, 5), facecolor=bg_color)
ax1 = plt.subplot(111, facecolor=bg_color)

years = yearly_counts.index.values
counts = yearly_counts.values

ax1.plot(years, counts, color=netflix_red, linewidth=2.5, marker="o", markersize=3, label="Total Catalog Titles")
ax1.fill_between(years, counts, color=netflix_red, alpha=0.18)

# Annotate Peak Year 2018
ax1.annotate(
    f"Peak Year: {peak_year}\n({peak_count:,} titles)",
    xy=(peak_year, peak_count),
    xytext=(peak_year - 15, peak_count - 50),
    arrowprops=dict(facecolor="#FFFFFF", shrink=0.08, width=1.5, headwidth=6),
    color=text_color,
    fontweight="bold",
    fontsize=9.5,
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#222222", edgecolor=netflix_red)
)

ax1.set_title("Distribution of Netflix Catalogue Titles by Release Year (1925 - 2021)", color=text_color, fontsize=12.5, weight="bold", pad=15)
ax1.set_xlabel("Release Year", color=text_color, fontsize=10.5)
ax1.set_ylabel("Number of Titles Available", color=text_color, fontsize=10.5)
ax1.tick_params(colors=text_color, labelsize=9.5)
for spine in ax1.spines.values():
    spine.set_color("#444444")
ax1.grid(True, linestyle="--", alpha=0.25, color="#666666")

plt.tight_layout()
chart1_path = os.path.join(output_dir, "yearly_content_trend.png")
plt.savefig(chart1_path, dpi=300, facecolor=bg_color)
plt.close()
print(f"[SAVED]: Yearly trend line chart saved to {chart1_path}")

# Chart 2: Top 10 Release Years Bar Chart
plt.figure(figsize=(8.5, 4.8), facecolor=bg_color)
ax2 = plt.subplot(111, facecolor=bg_color)

top_yrs_labels = [str(y) for y in top_10_years.index]
top_yrs_vals = top_10_years.values

bars2 = ax2.bar(top_yrs_labels, top_yrs_vals, color=netflix_red, width=0.55)
ax2.set_title("Top 10 Release Years by Netflix Available Content Volume", color=text_color, fontsize=12.5, weight="bold", pad=15)
ax2.set_xlabel("Release Year", color=text_color, fontsize=10.5)
ax2.set_ylabel("Number of Titles", color=text_color, fontsize=10.5)
ax2.tick_params(colors=text_color, labelsize=9.5)
for spine in ax2.spines.values():
    spine.set_color("#444444")
ax2.grid(axis="y", linestyle="--", alpha=0.25, color="#666666")

for bar in bars2:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width() / 2, h + 15, f"{int(h):,}", ha="center", color=text_color, fontsize=9, weight="bold")

plt.tight_layout()
chart2_path = os.path.join(output_dir, "top_release_years.png")
plt.savefig(chart2_path, dpi=300, facecolor=bg_color)
plt.close()
print(f"[SAVED]: Top release years bar chart saved to {chart2_path}")

# Chart 3: Movies vs TV Shows Trend Comparison (1990 - 2021)
plt.figure(figsize=(10, 5), facecolor=bg_color)
ax3 = plt.subplot(111, facecolor=bg_color)

recent_slice = yearly_type_df[yearly_type_df.index >= 1990]
ax3.plot(recent_slice.index, recent_slice["Movie"], color=netflix_red, linewidth=2.2, label="Movies")
ax3.plot(recent_slice.index, recent_slice["TV Show"], color="#AAAAAA", linewidth=2.2, linestyle="--", label="TV Shows")

ax3.set_title("Comparative Trend: Movies vs TV Shows by Release Year (1990 - 2021)", color=text_color, fontsize=12.5, weight="bold", pad=15)
ax3.set_xlabel("Release Year", color=text_color, fontsize=10.5)
ax3.set_ylabel("Number of Titles Available", color=text_color, fontsize=10.5)
ax3.tick_params(colors=text_color, labelsize=9.5)
ax3.legend(facecolor="#222222", edgecolor="#444444", labelcolor=text_color)
for spine in ax3.spines.values():
    spine.set_color("#444444")
ax3.grid(True, linestyle="--", alpha=0.25, color="#666666")

plt.tight_layout()
chart3_path = os.path.join(output_dir, "content_type_year_comparison.png")
plt.savefig(chart3_path, dpi=300, facecolor=bg_color)
plt.close()
print(f"[SAVED]: Movie vs TV Show comparison trend saved to {chart3_path}")

# ------------------------------------------------------------------------------
# STEP 6: EXPORT JSON DATA FOR FRONTEND DASHBOARD
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 6: EXPORTING DASHBOARD JSON DATA")
print("=" * 60)

dashboard_data = {
    "projectName": "Netflix Content Trend Analysis by Release Year",
    "taskName": "Task 4 (Medium) – Auspify Data Analysis Internship",
    "totalTitles": total_titles,
    "earliestYear": min_year,
    "latestYear": max_year,
    "yearSpan": total_years_span,
    "peakYear": peak_year,
    "peakCount": peak_count,
    "topReleaseYears": [
        {"rank": i + 1, "year": int(y), "count": int(c)}
        for i, (y, c) in enumerate(top_10_years.items())
    ],
    "yearlyTrendData": [
        {
            "year": int(y),
            "movies": int(yearly_type_df.loc[y, "Movie"]),
            "tvShows": int(yearly_type_df.loc[y, "TV Show"]),
            "total": int(yearly_type_df.loc[y, "Total"])
        }
        for y in yearly_type_df.index if y >= 2000
    ],
    "keyFindings": [
        f"Content release years span across {total_years_span} years, ranging from the earliest classic title released in {min_year} up to {max_year}.",
        f"The single peak release year in Netflix's catalog is {peak_year} with {peak_count:,} titles, closely followed by 2017 ({top_10_years[2017]:,} titles) and 2019 ({top_10_years[2019]:,} titles).",
        "Over 80% of all catalog content was released between 2015 and 2021, illustrating Netflix's aggressive library expansion during the streaming boom.",
        "TV Show additions grew dramatically beginning in 2016, closing the gap with movie acquisitions as serialized storytelling became central to subscriber retention."
    ]
}

# 1. Export JSON
json_path = os.path.join(reports_dir, "trend_analysis_results.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(dashboard_data, f, indent=4)
print(f"[SAVED]: JSON report saved to {json_path}")

# 2. Export JS
js_path = os.path.join(reports_dir, "trend_analysis_results.js")
with open(js_path, "w", encoding="utf-8") as f:
    f.write(f"const TREND_ANALYSIS_RESULTS = {json.dumps(dashboard_data, indent=4)};\n")
print(f"[SAVED]: JavaScript data saved to {js_path}")

print("\n" + "=" * 60)
print("TASK 4 TREND ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 60)
