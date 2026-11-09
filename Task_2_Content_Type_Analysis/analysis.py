# ==============================================================================
# PROJECT: NETFLIX CONTENT TYPE ANALYSIS DASHBOARD
# Task: Task 2 (Easy) - Auspify Data Analysis Using Python Internship
# Student: Priya Sharma
# Description: Analyze the distribution of Movies and TV Shows on Netflix
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
# STEP 1: LOAD THE CLEANED DATASET
# ------------------------------------------------------------------------------
print("=" * 60)
print("TASK 2: NETFLIX CONTENT TYPE ANALYSIS")
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

total_records = len(df)
print(f"Total titles loaded: {total_records}")
print("\nFirst 5 rows of Type column:")
print(df[["show_id", "type", "title"]].head())

# ------------------------------------------------------------------------------
# STEP 2: CALCULATE TOTAL MOVIES AND TV SHOWS
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 2: CALCULATING MOVIES AND TV SHOWS COUNT")
print("=" * 60)

# Standardize type column text
df["type"] = df["type"].astype(str).str.strip()

# Count each content type using value_counts()
type_counts = df["type"].value_counts()
movies_count = int(type_counts.get("Movie", 0))
tv_shows_count = int(type_counts.get("TV Show", 0))

print(f"Total Movies  : {movies_count}")
print(f"Total TV Shows: {tv_shows_count}")

# ------------------------------------------------------------------------------
# STEP 3: CALCULATE PROPORTIONS AND PERCENTAGES
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 3: CALCULATING CONTENT PERCENTAGES & RATIOS")
print("=" * 60)

movie_pct = round((movies_count / total_records) * 100, 2)
tv_show_pct = round((tv_shows_count / total_records) * 100, 2)
ratio = round(movies_count / tv_shows_count, 2) if tv_shows_count > 0 else 0

print(f"Movie Share  : {movie_pct}%")
print(f"TV Show Share: {tv_show_pct}%")
print(f"Movie to TV Show Ratio: {ratio} : 1")

# Save Summary Table CSV
df_summary = pd.DataFrame({
    "Content_Type": ["Movie", "TV Show"],
    "Total_Count": [movies_count, tv_shows_count]
})
summary_csv_path = os.path.join(output_dir, "content_type_summary.csv")
df_summary.to_csv(summary_csv_path, index=False)
print(f"\n[SAVED]: Summary table saved to {summary_csv_path}")

# Save Percentages Table CSV
df_percentages = pd.DataFrame({
    "Content_Type": ["Movie", "TV Show"],
    "Total_Count": [movies_count, tv_shows_count],
    "Percentage": [movie_pct, tv_show_pct]
})
percentages_csv_path = os.path.join(output_dir, "content_type_percentages.csv")
df_percentages.to_csv(percentages_csv_path, index=False)
print(f"[SAVED]: Percentages table saved to {percentages_csv_path}")

# ------------------------------------------------------------------------------
# STEP 4: CREATE VISUALIZATIONS (BAR CHART & PIE CHART)
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 4: GENERATING CHARTS (BAR CHART & PIE CHART)")
print("=" * 60)

# Colors matching Netflix Dark Theme
netflix_red = "#E50914"
netflix_dark_grey = "#333333"
text_color = "#FFFFFF"
bg_color = "#141414"

# 1. Bar Chart
plt.figure(figsize=(7, 5), facecolor=bg_color)
ax = plt.subplot(111, facecolor=bg_color)
bars = ax.bar(["Movies", "TV Shows"], [movies_count, tv_shows_count], color=[netflix_red, "#808080"], width=0.5)

ax.set_title("Netflix Content Distribution: Movies vs TV Shows", color=text_color, fontsize=14, weight="bold", pad=15)
ax.set_ylabel("Number of Titles", color=text_color, fontsize=11)
ax.tick_params(colors=text_color, labelsize=11)
for spine in ax.spines.values():
    spine.set_color("#444444")
ax.grid(axis="y", linestyle="--", alpha=0.3, color="#666666")

# Add count labels on top of bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 100, f"{height:,}", ha="center", color=text_color, fontsize=11, weight="bold")

plt.tight_layout()
bar_chart_path = os.path.join(output_dir, "content_type_bar_chart.png")
plt.savefig(bar_chart_path, dpi=300, facecolor=bg_color)
plt.close()
print(f"[SAVED]: Bar chart saved to {bar_chart_path}")

# 2. Pie Chart
plt.figure(figsize=(6, 6), facecolor=bg_color)
pie_colors = [netflix_red, "#555555"]
explode = (0.05, 0)

wedges, texts, autotexts = plt.pie(
    [movies_count, tv_shows_count],
    labels=["Movies", "TV Shows"],
    autopct="%1.1f%%",
    startangle=140,
    colors=pie_colors,
    explode=explode,
    textprops={"color": text_color, "fontsize": 12, "weight": "bold"}
)
for autotext in autotexts:
    autotext.set_color("#FFFFFF")
    autotext.set_fontsize(12)

plt.title("Proportion of Netflix Content (Percentage Share)", color=text_color, fontsize=14, weight="bold", pad=20)
plt.tight_layout()
pie_chart_path = os.path.join(output_dir, "content_type_pie_chart.png")
plt.savefig(pie_chart_path, dpi=300, facecolor=bg_color)
plt.close()
print(f"[SAVED]: Pie chart saved to {pie_chart_path}")

# ------------------------------------------------------------------------------
# STEP 5: EXPORT JSON RESULTS FOR THE WEB DASHBOARD
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 5: EXPORTING DASHBOARD JSON DATA")
print("=" * 60)

dashboard_data = {
    "projectName": "Netflix Content Type Analysis",
    "taskName": "Task 2 (Easy) – Auspify Data Analysis Internship",
    "totalRecords": total_records,
    "moviesCount": movies_count,
    "tvShowsCount": tv_shows_count,
    "moviePercentage": movie_pct,
    "tvShowPercentage": tv_show_pct,
    "ratio": ratio,
    "keyFindings": [
        f"Movies dominate the Netflix streaming catalog, representing {movies_count:,} titles ({movie_pct}% of total content).",
        f"TV Shows account for {tv_shows_count:,} titles ({tv_show_pct}% of total content).",
        f"Movies outnumber TV Shows by a ratio of {ratio} : 1, indicating that Netflix's catalog originated with a heavy emphasis on film acquisition before expanding episodic series."
    ]
}

# 1. Export JSON file
json_path = os.path.join(reports_dir, "analysis_results.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(dashboard_data, f, indent=4)
print(f"[SAVED]: JSON report saved to {json_path}")

# 2. Export JS file for direct local browser opening
js_path = os.path.join(reports_dir, "analysis_results.js")
with open(js_path, "w", encoding="utf-8") as f:
    f.write(f"const CONTENT_TYPE_RESULTS = {json.dumps(dashboard_data, indent=4)};\n")
print(f"[SAVED]: JavaScript data saved to {js_path}")

print("\n" + "=" * 60)
print("TASK 2 CONTENT TYPE ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 60)
