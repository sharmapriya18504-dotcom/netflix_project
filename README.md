# Netflix Data Analysis & Web Analytics Platform

A complete, professional Data Analytics internship project analyzing Netflix's catalog of movies and TV shows using Python, Pandas, HTML5, CSS3, JavaScript, and Chart.js.

---

## 📌 1. Project Introduction

This project was developed for a **Data Analytics Internship**. It combines:
1. **Python Data Engineering & Analysis (`analysis.py`)**: For programmatic data cleaning, datetime conversion, statistical summaries, and static plot generation.
2. **Interactive Netflix Web Dashboard (`index.html`)**: A lightweight web application built with **HTML5, CSS3, Vanilla JavaScript, and Chart.js**. It features a signature cinematic Netflix black-and-red design, interactive charts, live instant search, catalog modal popups, and an internship evaluation guide.

---

## 🎯 2. Project Objectives

1. **Understand Dataset Architecture**: Inspect rows, columns, data types, and check for missing values and duplicates.
2. **Perform Safe Data Cleaning**: Strip whitespace, handle placeholder values like `"Not Given"` appropriately, convert date strings to datetime objects, and verify that no valid records are dropped prematurely.
3. **Exploratory Data Analysis (EDA)**: Answer core business questions regarding content formats, international contributions (using `explode()`), full release year trends, audience age ratings, and genre popularity.
4. **Data Visualization**: Generate interactive Chart.js charts and static Matplotlib/Seaborn plots.
5. **Business Insights & Evaluation**: Compile verified findings and evaluation Q&A for academic and internship presentations.

---

## 🛠️ 3. Technologies Used

- **Frontend & Visuals**: HTML5, CSS3, Vanilla JavaScript (ES6), Chart.js
- **Data Engineering**: Python 3.10+, Pandas, NumPy
- **Static Charting**: Matplotlib, Seaborn
- **Development & Tools**: VS Code, Git, GitHub Pages Ready

---

## 🎨 4. Netflix Cinematic Design System

- **Main Background**: `#141414` (Deep Cinematic Netflix Black)
- **Navbar/Header**: `#0B0B0B` (Dark Charcoal with Frosted Glass Blur)
- **Brand Accent**: `#E50914` (Netflix Crimson Red)
- **Cards**: `#222222` with `#333333` subtle borders and red glow hover effects
- **Typography**: Clean white headings (`#FFFFFF`) with muted secondary text (`#B3B3B3`)

---

## 🌟 5. Unique Web Features

1. **Netflix Hero Spotlight Banner**: Displays a featured title with metadata badges, director information, and quick action buttons.
2. **6 Real-Time KPI Cards**: Total Titles (`8,790`), Movies (`6,126`), TV Shows (`2,664`), Total Countries (`122`), Top Genre (`International Movies`), Peak Release Year (`2018`).
3. **Interactive Chart.js Visualizations (Auspify Tasks 2 to 5)**:
   - **Task 2**: Content Type Breakdown (Donut Chart: Movies 69.7% vs TV Shows 30.3%)
   - **Task 3**: Top 10 Content Producing Countries (Horizontal Bar Chart with multi-country split & explode)
   - **Task 4**: Content Production Trend Over Time (Area Line Chart 1925–2021 with 2018 peak annotation)
   - **Task 5 (Step 2)**: Top 10 Most Common Genres (Exploded Counts Bar Chart)
   - **Task 5 (Step 1)**: Content Rating Distribution (Audience Targeting Bar Chart)
   - **Task 5 (Step 3)**: Comparative Rating Analysis Across Content Types (Movies vs. TV Shows Grouped Bar Chart)
4. **Interactive Catalog Explorer**:
   - Live Search: Instant filtering by title, director, country, or genre with zero page reload.
   - Type Filters: Switch between `All`, `Movies Only`, and `TV Shows Only`.
   - Dynamic Sorting: Sort by newest, oldest, or alphabetical order.
   - Pagination: Clean pagination showing 12 titles per page.
5. **Netflix-Style Movie Detail Modal**: Clicking on any movie card opens a frosted popup showing full director, country, rating, duration, and genre pills.
6. **CSV Export Button**: Download catalog data directly as a CSV file in browser.
7. **Internship Viva Mode**: Built-in guide covering project methodology and top evaluation questions with model answers.

---

## 📁 6. Project Structure

```text
Netflix_Data_Analysis_Internship/
│
├── data/
│   └── Dataset.csv               # Original raw Netflix dataset (preserved untouched)
│
├── results/
│   ├── cleaned_netflix.csv       # Cleaned dataset (8,790 records)
│   ├── business_insights.txt     # Factual business insights report
│   └── plots/                    # Static high-res PNG plots
│       ├── content_type.png          # Task 2 plot
│       ├── top_countries.png         # Task 3 plot
│       ├── release_year.png          # Task 4 plot
│       ├── top_genres.png            # Task 5 (Genres) plot
│       ├── ratings.png               # Task 5 (Ratings) plot
│       └── ratings_by_type.png       # Task 5 (Comparative) plot
│
├── index.html                    # ⭐ Main Web Dashboard (HTML5)
├── style.css                     # ⭐ Custom Netflix Stylesheet
├── app.js                        # ⭐ Interactive Logic, Search, Modals & Chart.js
├── data.js                       # ⭐ Verified dataset export (8,790 records)
├── analysis.py                   # Automated Python analysis script
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation & evaluation guide
```

---

## 🚀 7. How to Run the Dashboard

### Method 1: Direct Double-Click (Easiest & Fastest)
1. Open the project folder in your file explorer:
   `c:\Users\Priya Sharma\Netflix_Data_Analysis_Internship`
2. Double-click **`index.html`**.
3. It will immediately open in your default browser (Chrome, Edge, Firefox, Brave) — **no installation or server needed!**

---

### Method 2: Using Python Local Server
In your VS Code terminal:
```bash
python -m http.server 8000
```
Open your browser and navigate to:
👉 **`http://localhost:8000`**

---

### Method 3: Running the Python Analysis Script
To run the headless batch analysis script:
```bash
python analysis.py
```

---

## 📊 8. Verified Analytical Results (From Real Dataset)

1. **Catalog Composition**:
   - **Movies**: 6,126 titles (69.69%)
   - **TV Shows**: 2,664 titles (30.31%)
   - **Total**: 8,790 titles
2. **Top 5 Content Producing Nations**:
   - 1. United States: 3,240 titles
   - 2. India: 1,057 titles *(#1 in Asia, #2 globally)*
   - 3. United Kingdom: 638 titles
   - 4. Pakistan: 421 titles
   - 5. Canada: 271 titles
3. **Release Year Timeline**:
   - Spans 74 years from **1925 to 2021**.
   - Peak releases occurred in **2018 (1,146 titles)**.
4. **Audience Ratings**:
   - TV-MA (3,205 titles, 36.46%) and TV-14 (2,157 titles, 24.54%) represent **61.00%** of all content.
5. **Top Genres**:
   - International Movies (2,752), Dramas (2,426), Comedies (1,674), International TV Shows (1,349).

---

## 🌐 9. How to Deploy on GitHub Pages (For Resume Portfolio)

1. Push this project folder to your GitHub repository.
2. In your GitHub repository, click **Settings** ➔ **Pages** (in left sidebar).
3. Under **Branch**, select `main` (or `master`) and folder `/ (root)` ➔ click **Save**.
4. In 1–2 minutes, GitHub will give you a public URL like:
   `https://<your-username>.github.io/<repo-name>/`
5. You can put this live link directly on your **Resume**, **LinkedIn**, and **Internship Project Submission**!
