# ==============================================================================
# PROJECT: NETFLIX COUNTRY-WISE CONTENT ANALYSIS
# Task: Task 3 (Medium) - Auspify Data Analysis Using Python Internship
# Student: Priya Sharma
# Description: Analyze Netflix catalogue content availability across countries
# ==============================================================================

import os
import json
import numpy as np
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
print("TASK 3: NETFLIX COUNTRY-WISE CONTENT ANALYSIS")
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
print(f"Total titles in dataset: {total_titles}")

# ------------------------------------------------------------------------------
# STEP 2: EXTRACT AND CLEAN COUNTRY INFORMATION
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 2: EXTRACTING & CLEANING COUNTRY DATA")
print("=" * 60)

# Identify missing or "Not Given" country records
missing_country_mask = df["country"].isna() | (df["country"].astype(str).str.strip() == "Not Given")
missing_country_count = int(missing_country_mask.sum())
valid_country_count = total_titles - missing_country_count

print(f"Titles with available country info: {valid_country_count}")
print(f"Titles without country info (Not Given / NaN): {missing_country_count} ({round((missing_country_count / total_titles) * 100, 2)}%)")

# Filter only titles with valid country information
df_valid_country = df[~missing_country_mask].copy()

# A single title can list multiple countries separated by comma (e.g. 'United States, India')
# We split by comma and use explode() so each country gets credit
df_valid_country["country_list"] = df_valid_country["country"].astype(str).str.split(",")
df_exploded = df_valid_country.explode("country_list").copy()
df_exploded["clean_country"] = df_exploded["country_list"].astype(str).str.strip()

# Remove any accidental empty strings
df_exploded = df_exploded[df_exploded["clean_country"] != ""]
df_exploded = df_exploded[df_exploded["clean_country"] != "Not Given"]

unique_countries = df_exploded["clean_country"].nunique()
print(f"Total distinct countries represented in Netflix catalogue: {unique_countries}")

# ------------------------------------------------------------------------------
# STEP 3: IDENTIFY TOP 10 COUNTRIES & CALCULATE RANKINGS
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 3: IDENTIFYING TOP 10 COUNTRIES")
print("=" * 60)

country_counts = df_exploded["clean_country"].value_counts()
top_10_series = country_counts.head(10)

print("\n--- Top 10 Countries by Available Titles ---")
for rank, (country, count) in enumerate(top_10_series.items(), 1):
    print(f"  {rank}. {country:20}: {count} titles")

# ------------------------------------------------------------------------------
# STEP 4: COMPARE CONTENT TYPES (MOVIES VS TV SHOWS) ACROSS TOP COUNTRIES
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 4: COMPARING CONTENT TYPES ACROSS TOP COUNTRIES")
print("=" * 60)

top_10_names = top_10_series.index.tolist()
df_top_10 = df_exploded[df_exploded["clean_country"].isin(top_10_names)]

# Group by country and type
country_type_df = df_top_10.groupby(["clean_country", "type"]).size().unstack(fill_value=0)
country_type_df["Total"] = country_type_df.sum(axis=1)

# Ensure columns 'Movie' and 'TV Show' exist
if "Movie" not in country_type_df.columns:
    country_type_df["Movie"] = 0
if "TV Show" not in country_type_df.columns:
    country_type_df["TV Show"] = 0

# Sort by Total descending
country_type_df = country_type_df.loc[top_10_names]
print("\n--- Content Type Breakdown for Top 10 Countries ---")
print(country_type_df[["Movie", "TV Show", "Total"]])

# ------------------------------------------------------------------------------
# STEP 5: SAVE OUTPUT CSVS
# ------------------------------------------------------------------------------
# 1. Full Country Content Summary
df_all_countries = country_counts.reset_index()
df_all_countries.columns = ["Country", "Content_Count"]
all_countries_csv = os.path.join(output_dir, "country_content_summary.csv")
df_all_countries.to_csv(all_countries_csv, index=False)
print(f"\n[SAVED]: Full country summary saved to {all_countries_csv}")

# 2. Top 10 Countries CSV
df_top_10_csv = top_10_series.reset_index()
df_top_10_csv.columns = ["Country", "Content_Count"]
df_top_10_csv["Rank"] = range(1, 11)
df_top_10_csv = df_top_10_csv[["Rank", "Country", "Content_Count"]]
top_10_csv = os.path.join(output_dir, "top_10_countries.csv")
df_top_10_csv.to_csv(top_10_csv, index=False)
print(f"[SAVED]: Top 10 countries saved to {top_10_csv}")

# 3. Country vs Type Comparison CSV
df_comparison_export = country_type_df.reset_index()
df_comparison_export.columns = ["Country", "Movie_Count", "TV_Show_Count", "Total_Count"]
comp_csv = os.path.join(output_dir, "country_type_comparison.csv")
df_comparison_export.to_csv(comp_csv, index=False)
print(f"[SAVED]: Country type comparison saved to {comp_csv}")

# ------------------------------------------------------------------------------
# STEP 6: GENERATE MATPLOTLIB CHARTS
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 6: GENERATING CHARTS")
print("=" * 60)

netflix_red = "#E50914"
netflix_grey = "#555555"
bg_color = "#141414"
text_color = "#FFFFFF"

# Chart 1: Top 10 Countries Horizontal Bar Chart
plt.figure(figsize=(9, 5.5), facecolor=bg_color)
ax1 = plt.subplot(111, facecolor=bg_color)

# Reverse so rank 1 is on top
y_countries = list(reversed(top_10_series.index.tolist()))
x_counts = list(reversed(top_10_series.values.tolist()))

bars1 = ax1.barh(y_countries, x_counts, color=netflix_red, height=0.6)
ax1.set_title("Top 10 Countries by Netflix Catalogue Content Volume", color=text_color, fontsize=13, weight="bold", pad=15)
ax1.set_xlabel("Number of Titles Available", color=text_color, fontsize=11)
ax1.tick_params(colors=text_color, labelsize=10)
for spine in ax1.spines.values():
    spine.set_color("#444444")
ax1.grid(axis="x", linestyle="--", alpha=0.3, color="#666666")

for bar in bars1:
    width = bar.get_width()
    ax1.text(width + 30, bar.get_y() + bar.get_height() / 2, f"{int(width):,}", va="center", color=text_color, fontsize=10, weight="bold")

plt.tight_layout()
chart1_path = os.path.join(output_dir, "top_10_countries.png")
plt.savefig(chart1_path, dpi=300, facecolor=bg_color)
plt.close()
print(f"[SAVED]: Top 10 bar chart saved to {chart1_path}")

# Chart 2: Movies vs TV Shows Grouped Comparison for Top Countries
plt.figure(figsize=(10, 5.5), facecolor=bg_color)
ax2 = plt.subplot(111, facecolor=bg_color)

x = np.arange(len(top_10_names))
bar_width = 0.38

movies_vals = country_type_df["Movie"].values
tv_vals = country_type_df["TV Show"].values

ax2.bar(x - bar_width/2, movies_vals, bar_width, label="Movies", color=netflix_red)
ax2.bar(x + bar_width/2, tv_vals, bar_width, label="TV Shows", color="#777777")

ax2.set_title("Movies vs TV Shows in Top 10 Netflix Content Countries", color=text_color, fontsize=13, weight="bold", pad=15)
ax2.set_xticks(x)
ax2.set_xticklabels(top_10_names, rotation=35, ha="right", color=text_color, fontsize=9.5)
ax2.tick_params(colors=text_color)
ax2.legend(facecolor="#222222", edgecolor="#444444", labelcolor=text_color)
for spine in ax2.spines.values():
    spine.set_color("#444444")
ax2.grid(axis="y", linestyle="--", alpha=0.3, color="#666666")

plt.tight_layout()
chart2_path = os.path.join(output_dir, "country_type_breakdown.png")
plt.savefig(chart2_path, dpi=300, facecolor=bg_color)
plt.close()
print(f"[SAVED]: Country content type breakdown chart saved to {chart2_path}")

# ------------------------------------------------------------------------------
# STEP 7: EXPORT JSON DATA FOR FRONTEND DASHBOARD
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 7: EXPORTING DASHBOARD JSON DATA")
print("=" * 60)

dashboard_data = {
    "projectName": "Netflix Country-Wise Content Analysis",
    "taskName": "Task 3 (Medium) – Auspify Data Analysis Internship",
    "totalTitles": total_titles,
    "validTitles": valid_country_count,
    "missingTitles": missing_country_count,
    "totalCountries": unique_countries,
    "topCountryName": top_10_names[0],
    "topCountryCount": int(top_10_series.values[0]),
    "top10Countries": [
        {"rank": i + 1, "country": country, "count": int(count)}
        for i, (country, count) in enumerate(top_10_series.items())
    ],
    "countryTypeComparison": [
        {
            "country": c,
            "movies": int(country_type_df.loc[c, "Movie"]),
            "tvShows": int(country_type_df.loc[c, "TV Show"]),
            "total": int(country_type_df.loc[c, "Total"])
        }
        for c in top_10_names
    ],
    "businessInsights": [
        f"The United States holds the largest share of Netflix catalogue titles ({top_10_series['United States']:,} titles), followed by India ({top_10_series['India']:,} titles) and the United Kingdom ({top_10_series['United Kingdom']:,} titles).",
        f"India is the dominant Asian content contributor with {top_10_series['India']:,} titles, consisting predominantly of feature movies over TV shows.",
        "In contrast, countries like South Korea and Japan exhibit a much stronger balance towards TV Shows and anime series, reflecting localized consumption trends.",
        f"{missing_country_count} titles ({round((missing_country_count / total_titles) * 100, 2)}%) lacked verified country metadata ('Not Given') and were excluded from country aggregations to prevent distortion."
    ]
}

# 1. Export JSON
json_path = os.path.join(reports_dir, "country_analysis_results.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(dashboard_data, f, indent=4)
print(f"[SAVED]: JSON report saved to {json_path}")

# 2. Export JS
js_path = os.path.join(reports_dir, "country_analysis_results.js")
with open(js_path, "w", encoding="utf-8") as f:
    f.write(f"const COUNTRY_ANALYSIS_RESULTS = {json.dumps(dashboard_data, indent=4)};\n")
print(f"[SAVED]: JavaScript data saved to {js_path}")

print("\n" + "=" * 60)
print("TASK 3 COUNTRY ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 60)
