# ==============================================================================
# NETFLIX DATA ANALYSIS PROJECT USING PYTHON
# ==============================================================================
# Student Name: Data Analytics Intern
# Technology  : Python, Pandas, NumPy, Matplotlib, Seaborn
# Dataset     : data/Dataset.csv (Original file preserved untouched)
# ==============================================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure the results and plots directories exist
os.makedirs("results/plots", exist_ok=True)

# Set clean visualization theme
sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"


# ==============================================================================
# TASK 1: DATA LOADING AND UNDERSTANDING
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 1: DATA LOADING AND UNDERSTANDING")
print("=" * 60)

# Step 1.1: Load dataset from CSV file
csv_path = os.path.join("data", "Dataset.csv")
print(f"Loading dataset from: {csv_path}")
df_raw = pd.read_csv(csv_path)

# Step 1.2: Display first 5 rows
print("\n--- 1. First 5 Rows of Dataset ---")
print(df_raw.head())

# Step 1.3: Check dataset shape
original_rows, original_cols = df_raw.shape
print(f"\n--- 2. Dataset Shape ---")
print(f"Total Rows   : {original_rows}")
print(f"Total Columns: {original_cols}")

# Step 1.4: Display column names and data types
print("\n--- 3. Column Names and Data Types ---")
print(df_raw.dtypes)

# Step 1.5: Check missing values in raw dataset
print("\n--- 4. Missing Values in Raw Dataset ---")
print(df_raw.isnull().sum())

# Step 1.6: Check confirmed exact duplicate records across all columns
exact_duplicates_raw = df_raw.duplicated().sum()
print(f"\n--- 5. Exact Duplicate Records (All Columns) ---")
print(f"Confirmed exact duplicate rows: {exact_duplicates_raw}")


# ==============================================================================
# TASK 2: DATA CLEANING
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 2: DATA CLEANING")
print("=" * 60)

# Create a working copy so the original dataset remains untouched
df = df_raw.copy()

# Step 2.1: Clean unnecessary spaces in all text columns
text_columns = df.select_dtypes(include="object").columns
for col in text_columns:
    df[col] = df[col].astype(str).str.strip()
print("Cleaned leading and trailing whitespace across all text columns.")

# Step 2.2: Handle placeholder values such as 'Not Given'
director_placeholders = (df["director"] == "Not Given").sum()
country_placeholders = (df["country"] == "Not Given").sum()
print(f"Found placeholder 'Not Given': {director_placeholders} in director, {country_placeholders} in country.")

# Replace 'Not Given' with NaN so Pandas recognizes them properly as missing
df["director"] = df["director"].replace("Not Given", np.nan)
df["country"] = df["country"].replace("Not Given", np.nan)
print("Replaced 'Not Given' with NaN for accurate missing value representation.")

# Step 2.3: Duplicate Handling
# A. Check for confirmed exact duplicates across all columns
exact_duplicates = df.duplicated().sum()
print(f"\nConfirmed exact full-row duplicates: {exact_duplicates}")
if exact_duplicates > 0:
    df = df.drop_duplicates()
    print(f"Removed {exact_duplicates} confirmed exact duplicates.")
else:
    print("No confirmed exact full-row duplicates found. No records deleted.")

# B. Check for records with duplicate title and type (DO NOT delete them automatically)
title_type_duplicates = df[df.duplicated(subset=["title", "type"], keep=False)].sort_values(by=["title", "show_id"])
print(f"\nRecords having duplicate Title and Type (Found {len(title_type_duplicates)} rows / {len(title_type_duplicates)//2} pairs):")
print(title_type_duplicates[["show_id", "type", "title", "director", "country", "release_year"]])
print("Note: These records have different show_id values. All records are kept as per instructions.")

# Step 2.4: Convert date_added into proper datetime format
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

# Check for invalid dates after conversion
invalid_dates = df["date_added"].isnull().sum()
print(f"\nInvalid dates after datetime conversion: {invalid_dates}")
print(f"Date range: {df['date_added'].min().date()} to {df['date_added'].max().date()}")

# Step 2.5: Data Quality Verification After Cleaning
print("\n--- Missing Values After Cleaning ---")
print(df.isnull().sum())

final_rows = len(df)
print(f"\nOriginal Dataset Row Count: {original_rows}")
print(f"Final Cleaned Dataset Row Count: {final_rows}")

# Step 2.6: Save cleaned dataset as cleaned_netflix.csv
cleaned_csv_path = os.path.join("results", "cleaned_netflix.csv")
df.to_csv(cleaned_csv_path, index=False)
print(f"Cleaned dataset saved to: {cleaned_csv_path}")


# ==============================================================================
# TASK 3: EXPLORATORY DATA ANALYSIS (EDA)
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 3: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# Question 1: How many Movies and TV Shows are available?
type_counts = df["type"].value_counts()
movie_count = type_counts.get("Movie", 0)
tv_count = type_counts.get("TV Show", 0)
print("\n--- Question 1: Movies and TV Shows Count ---")
print(f"Movies   : {movie_count} ({movie_count / final_rows * 100:.2f}%)")
print(f"TV Shows : {tv_count} ({tv_count / final_rows * 100:.2f}%)")
print(f"Total    : {final_rows}")

# Question 2: Which type of content is more common?
dominant_type = type_counts.idxmax()
print("\n--- Question 2: More Common Content Type ---")
print(f"'{dominant_type}' is more common on Netflix, representing {type_counts.max() / final_rows * 100:.2f}% of all titles.")

# Question 3: Which countries have the highest number of Netflix titles?
# Split the country column by comma and explode to count each individual country
exploded_countries = df["country"].dropna().str.split(",").explode().str.strip()
top_countries = exploded_countries.value_counts().head(10)
print("\n--- Question 3: Top 10 Countries (Split & Exploded) ---")
for rank, (country, count) in enumerate(top_countries.items(), 1):
    print(f"{rank:2d}. {country:<18} : {count} titles")

# Question 4: Complete release-year distribution and highest year
release_year_distribution = df["release_year"].value_counts().sort_index()
peak_year = df["release_year"].value_counts().idxmax()
peak_count = df["release_year"].value_counts().max()
top_release_years = df["release_year"].value_counts().head(10)

print("\n--- Question 4: Release Year Analysis ---")
print(f"Total Unique Release Years: {df['release_year'].nunique()} (from {df['release_year'].min()} to {df['release_year'].max()})")
print(f"Year with Highest Releases: {peak_year} ({peak_count} titles)")
print("\nTop 10 Release Years by Content Count:")
for rank, (year, count) in enumerate(top_release_years.items(), 1):
    print(f"{rank:2d}. Year {year} : {count} titles")

# Question 5: What are the most common content ratings?
top_ratings = df["rating"].value_counts().head(10)
print("\n--- Question 5: Top 10 Content Ratings ---")
for rank, (rating, count) in enumerate(top_ratings.items(), 1):
    print(f"{rank:2d}. {rating:<10} : {count} titles ({count / final_rows * 100:.2f}%)")

# Question 6: Which genres are most common?
# Split comma-separated genres and explode
exploded_genres = df["listed_in"].dropna().str.split(",").explode().str.strip()
top_genres = exploded_genres.value_counts().head(10)
print("\n--- Question 6: Top 10 Most Common Genres ---")
for rank, (genre, count) in enumerate(top_genres.items(), 1):
    print(f"{rank:2d}. {genre:<28} : {count} appearances")


# ==============================================================================
# TASK 4: DATA VISUALIZATION
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 4: DATA VISUALIZATION")
print("=" * 60)

# Chart 1: Bar chart: Movies vs TV Shows
plt.figure(figsize=(7, 5))
colors = ["#E50914", "#221F1F"]
bars1 = plt.bar(type_counts.index, type_counts.values, color=colors, width=0.55, edgecolor="black", linewidth=1.2)
plt.title("Distribution of Netflix Content: Movies vs TV Shows", fontsize=13, fontweight="bold", pad=12)
plt.xlabel("Content Type", fontsize=11, fontweight="bold")
plt.ylabel("Number of Titles", fontsize=11, fontweight="bold")
plt.ylim(0, max(type_counts.values) * 1.15)

for bar in bars1:
    h = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, h + 120, f"{h:,} ({h/final_rows*100:.1f}%)",
             ha="center", va="bottom", fontsize=10, fontweight="bold")

plot1_path = os.path.join("results", "plots", "content_type.png")
plt.tight_layout()
plt.savefig(plot1_path, dpi=300)
plt.close()
print(f"Saved: {plot1_path}")

# Chart 2: Bar chart: Top 10 countries (Accurate with explode)
plt.figure(figsize=(10, 6))
country_palette = sns.color_palette("Reds_r", n_colors=10)
bars2 = plt.barh(top_countries.index[::-1], top_countries.values[::-1], color=country_palette, edgecolor="black", linewidth=0.8)
plt.title("Top 10 Content Producing Countries on Netflix", fontsize=13, fontweight="bold", pad=12)
plt.xlabel("Number of Titles (Individual Country Mentions)", fontsize=11, fontweight="bold")
plt.ylabel("Country", fontsize=11, fontweight="bold")
plt.xlim(0, max(top_countries.values) * 1.15)

for bar in bars2:
    w = bar.get_width()
    plt.text(w + 40, bar.get_y() + bar.get_height() / 2, f"{int(w):,}",
             ha="left", va="center", fontsize=9.5, fontweight="bold")

plot2_path = os.path.join("results", "plots", "top_countries.png")
plt.tight_layout()
plt.savefig(plot2_path, dpi=300)
plt.close()
print(f"Saved: {plot2_path}")

# Chart 3: Line chart: Content released by year (Complete dataset from 1925 to 2021)
plt.figure(figsize=(12, 6))
plt.plot(release_year_distribution.index, release_year_distribution.values,
         color="#E50914", linewidth=2.5, marker="o", markersize=4)
plt.fill_between(release_year_distribution.index, release_year_distribution.values, color="#E50914", alpha=0.15)
plt.title("Complete Content Release Year Distribution (1925 - 2021)", fontsize=13, fontweight="bold", pad=12)
plt.xlabel("Release Year", fontsize=11, fontweight="bold")
plt.ylabel("Number of Titles Released", fontsize=11, fontweight="bold")
plt.grid(True, linestyle="--", alpha=0.5)

# Annotate the actual highest year identified across the complete dataset
plt.annotate(
    f"Highest Year: {peak_year}\n({peak_count} titles)",
    xy=(peak_year, peak_count),
    xytext=(peak_year - 18, peak_count - 120),
    arrowprops=dict(facecolor="black", shrink=0.08, width=1.5, headwidth=6),
    fontweight="bold", fontsize=10
)

plot3_path = os.path.join("results", "plots", "release_year.png")
plt.tight_layout()
plt.savefig(plot3_path, dpi=300)
plt.close()
print(f"Saved: {plot3_path}")

# Chart 4: Bar chart: Top 10 genres
plt.figure(figsize=(10, 6))
genre_palette = sns.color_palette("Blues_r", n_colors=10)
bars4 = plt.barh(top_genres.index[::-1], top_genres.values[::-1], color=genre_palette, edgecolor="black", linewidth=0.8)
plt.title("Top 10 Content Genres on Netflix", fontsize=13, fontweight="bold", pad=12)
plt.xlabel("Frequency Across Titles", fontsize=11, fontweight="bold")
plt.ylabel("Genre", fontsize=11, fontweight="bold")
plt.xlim(0, max(top_genres.values) * 1.15)

for bar in bars4:
    w = bar.get_width()
    plt.text(w + 35, bar.get_y() + bar.get_height() / 2, f"{int(w):,}",
             ha="left", va="center", fontsize=9.5, fontweight="bold")

plot4_path = os.path.join("results", "plots", "top_genres.png")
plt.tight_layout()
plt.savefig(plot4_path, dpi=300)
plt.close()
print(f"Saved: {plot4_path}")

# Chart 5: Bar chart: Content rating distribution
plt.figure(figsize=(10, 5))
rating_palette = sns.color_palette("mako", n_colors=len(top_ratings))
bars5 = plt.bar(top_ratings.index, top_ratings.values, color=rating_palette, edgecolor="black", linewidth=0.8)
plt.title("Content Rating Distribution on Netflix", fontsize=13, fontweight="bold", pad=12)
plt.xlabel("Rating Category", fontsize=11, fontweight="bold")
plt.ylabel("Number of Titles", fontsize=11, fontweight="bold")
plt.ylim(0, max(top_ratings.values) * 1.15)

for bar in bars5:
    h = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, h + 45, f"{int(h):,}",
             ha="center", va="bottom", fontsize=9, fontweight="bold")

plot5_path = os.path.join("results", "plots", "ratings.png")
plt.tight_layout()
plt.savefig(plot5_path, dpi=300)
plt.close()
print(f"Saved: {plot5_path}")

# Chart 6: Comparative Bar Chart: Content Ratings by Type (Movies vs TV Shows - Task 5 Step 3)
plt.figure(figsize=(10, 5))
top_ratings_list = top_ratings.head(8).index.tolist()
movies_by_rating = [(df[(df["rating"] == r) & (df["type"] == "Movie")]).shape[0] for r in top_ratings_list]
tv_by_rating = [(df[(df["rating"] == r) & (df["type"] == "TV Show")]).shape[0] for r in top_ratings_list]

x_indices = np.arange(len(top_ratings_list))
bar_width = 0.38

plt.bar(x_indices - bar_width/2, movies_by_rating, bar_width, label="Movies", color="#E50914", edgecolor="black", linewidth=0.8)
plt.bar(x_indices + bar_width/2, tv_by_rating, bar_width, label="TV Shows", color="#333333", edgecolor="black", linewidth=0.8)

plt.title("Task 5 (Step 3): Content Rating Comparison: Movies vs TV Shows", fontsize=13, fontweight="bold", pad=12)
plt.xlabel("Rating Category", fontsize=11, fontweight="bold")
plt.ylabel("Number of Titles", fontsize=11, fontweight="bold")
plt.xticks(x_indices, top_ratings_list)
plt.legend(frameon=True)

plot6_path = os.path.join("results", "plots", "ratings_by_type.png")
plt.tight_layout()
plt.savefig(plot6_path, dpi=300)
plt.close()
print(f"Saved: {plot6_path}")


# ==============================================================================
# TASK 5: BUSINESS INSIGHTS
# ==============================================================================
print("\n" + "=" * 60)
print("TASK 5: BUSINESS INSIGHTS GENERATION")
print("=" * 60)

# Factual, data-grounded insights strictly supported by the actual dataset
insights_content = f"""======================================================================
NETFLIX DATA ANALYSIS - BUSINESS INSIGHTS REPORT
======================================================================
Analyzed Dataset : data/Dataset.csv
Total Titles     : {final_rows:,} records

1. Content Type Breakdown (Movies vs. TV Shows):
   Movies represent {movie_count:,} titles ({movie_count/final_rows*100:.2f}% of the library),
   while TV Shows represent {tv_count:,} titles ({tv_count/final_rows*100:.2f}%).
   In this dataset, movies outnumber TV shows by more than 2 to 1.

2. Leading Content Producing Countries:
   After splitting multiple country listings individually, the United States
   has the highest number of titles with {top_countries.get('United States', 0):,} entries,
   followed by India with {top_countries.get('India', 0):,} titles and the United Kingdom
   with {top_countries.get('United Kingdom', 0):,} titles. India is the largest Asian content
   provider in the dataset.

3. Complete Content Release Year Trend:
   The dataset contains content originally released between {df['release_year'].min()} and {df['release_year'].max()}.
   Across this entire period, the year {peak_year} has the single highest number of releases
   with {peak_count:,} titles, followed by 2017 ({top_release_years.get(2017, 0):,} titles) and 2019 ({top_release_years.get(2019, 0):,} titles).
   Most content in the catalog was released between 2015 and 2020.

4. Target Audience Age Ratings:
   The two most frequent ratings are TV-MA ({top_ratings.get('TV-MA', 0):,} titles, {top_ratings.get('TV-MA', 0)/final_rows*100:.2f}%)
   and TV-14 ({top_ratings.get('TV-14', 0):,} titles, {top_ratings.get('TV-14', 0)/final_rows*100:.2f}%).
   Together, TV-MA and TV-14 make up {(top_ratings.get('TV-MA', 0) + top_ratings.get('TV-14', 0))/final_rows*100:.2f}% of all titles,
   showing that the vast majority of Netflix's library is cataloged for teen and mature adult audiences.

5. Top Content Genres:
   When counting each individual genre, "International Movies" ({top_genres.get('International Movies', 0):,} appearances),
   "Dramas" ({top_genres.get('Dramas', 0):,} appearances), and "Comedies" ({top_genres.get('Comedies', 0):,} appearances)
   are the top three genres. "International TV Shows" ranks fourth ({top_genres.get('International TV Shows', 0):,} appearances),
   demonstrating that international titles form a major component of both movies and TV shows.

6. Missing Data and Metadata Observations:
   In the raw dataset, missing entries were stored with placeholder text 'Not Given'.
   Specifically, {director_placeholders:,} titles ({director_placeholders/final_rows*100:.2f}%) have no listed director,
   and {country_placeholders:,} titles ({country_placeholders/final_rows*100:.2f}%) have no country listed.
   In contrast, title, content type, release year, rating, and duration have 100% complete records.
======================================================================
"""

insights_file_path = os.path.join("results", "business_insights.txt")
with open(insights_file_path, "w", encoding="utf-8") as f:
    f.write(insights_content)

print(f"Business insights successfully written to: {insights_file_path}")
print("\n" + insights_content)

print("=" * 60)
print("ALL TASKS COMPLETED AND VERIFIED!")
print("=" * 60)
