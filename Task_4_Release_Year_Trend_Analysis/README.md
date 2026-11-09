# 📈 Task 4: Netflix Content Trend Analysis by Release Year
### Auspify Data Analysis Using Python Internship — Task 4 (Medium)

## 📌 1. About the Project
This project explores the historical distribution of titles across the Netflix catalog by their original **release year**, covering almost a century of cinematic and television history from **1925 to 2021**.

## 🎯 2. Project Objective
- Group and count catalog titles by `release_year` using Pandas `groupby()`.
- Identify historical growth patterns, peak acquisition periods, and decline trends.
- Determine the Top 10 release years with the greatest content density.
- Compare the growth trajectories of standalone Movies versus episodic TV Shows.
- Generate publication-quality Matplotlib line & bar charts and an interactive web dashboard.

## 🛠️ 3. Tools & Technologies Used
- **Language**: Python 3.x
- **Data Manipulation**: Pandas, NumPy
- **Visualizations**: Matplotlib (Python), Chart.js (Web)
- **Frontend Dashboard**: HTML5, CSS3, Vanilla JavaScript

## 🔍 4. Step-by-Step Analysis Workflow
1. **Load Data**: Cleaned Netflix dataset with 8,790 records.
2. **Verify Year Range**: Content spans from 1925 (earliest classic film) to 2021 (contemporary titles).
3. **Identify Peak Year**:
   - The all-time peak year in the catalog is **2018 with 1,146 titles**.
   - Followed closely by **2019** (1,030 titles) and **2017** (1,030 titles).
4. **Format Shift Over Time**:
   - Movies grew rapidly between 2014 and 2018.
   - TV Show additions accelerated strongly starting in 2016. In **2021**, TV Show releases (**315 titles**) outpaced Movie acquisitions (**277 titles**), showing Netflix's strategic pivot toward serialized content.
5. **Export Deliverables**: Created summary CSVs, rankings, line/bar charts, and JSON dashboard reports.

## 🚀 5. How to Run the Project

### Step 1: Run the Python Analysis
Open terminal inside the `Task_4_Release_Year_Trend_Analysis/` folder:
```bash
python trend_analysis.py
```
*This will execute the analysis and generate all CSV, PNG, and JSON deliverables in `output/` and `reports/`.*

### Step 2: Open the Dashboard
- **Direct**: Double click `index.html` in File Explorer.
- **Local Server**:
  ```bash
  python -m http.server 8000
  ```
  Visit `http://localhost:8000` in your web browser.

## 📁 6. Generated Output Files
- `output/yearly_content_summary.csv`
- `output/top_release_years.csv`
- `output/yearly_content_trend.png`
- `output/top_release_years.png`
- `output/content_type_year_comparison.png`
- `reports/trend_analysis_results.json`
- `reports/trend_analysis_results.js`

## 💡 7. What I Learned
- How to group and aggregate chronological data in Pandas using `groupby("release_year").size()`.
- How to perform two-dimensional time-series reshaping using `unstack()`.
- How to create annotated Matplotlib line plots highlighting peak values and historical milestones.
- The critical business distinction between when a title was released (`release_year`) versus when it was ingested into a streaming platform (`date_added`).
