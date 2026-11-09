# 🌍 Task 3: Netflix Country-Wise Content Analysis
### Auspify Data Analysis Using Python Internship — Task 3 (Medium)

## 📌 1. About the Project
This project explores the geographical distribution of Netflix catalogue titles across international markets. It examines which countries have the largest presence, analyzes multi-country co-productions, and investigates localized preferences between feature Movies and TV Shows.

## 🎯 2. Project Objective
- Extract and clean country metadata, properly splitting multi-country entries (e.g. `United States, India`) using Pandas `explode()`.
- Filter out unavailable country records (`"Not Given"` / `NaN`) to prevent statistical bias.
- Determine the top 10 countries by available titles in the Netflix catalogue.
- Analyze the ratio of Movies versus TV Shows in leading content hubs.
- Generate high-resolution Matplotlib charts and an interactive Netflix-styled web dashboard.

## 🛠️ 3. Tools & Technologies Used
- **Language**: Python 3.x
- **Data Manipulation**: Pandas, NumPy
- **Visualizations**: Matplotlib (Python), Chart.js (Web)
- **Frontend Dashboard**: HTML5, CSS3, Vanilla JavaScript

## 🔍 4. Step-by-Step Analysis Workflow
1. **Load Data**: Cleaned Netflix dataset with 8,790 records.
2. **Handle Multi-Country Entries**:
   - 287 titles had `"Not Given"` country info and were safely separated.
   - For valid titles, multiple comma-separated countries were exploded to grant equal credit to each participating country.
3. **Identify Top Countries**:
   - **United States**: 3,240 titles (2,395 Movies, 845 TV Shows)
   - **India**: 1,057 titles (976 Movies, 81 TV Shows)
   - **United Kingdom**: 638 titles (387 Movies, 251 TV Shows)
   - **Pakistan**: 421 titles (71 Movies, 350 TV Shows)
   - **Canada**: 271 titles (187 Movies, 84 TV Shows)
4. **Content Format Breakdown**:
   - Western countries (US, UK, Canada) and India show higher movie concentrations.
   - Countries like South Korea, Japan, and Pakistan show strong concentrations of TV Shows and episodic series.
5. **Export Deliverables**: Created summary CSVs, rankings, charts, and JSON reports.

## 🚀 5. How to Run the Project

### Step 1: Run the Python Analysis
Open terminal inside the `Task_3_Country_Wise_Analysis/` folder:
```bash
python country_analysis.py
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
- `output/country_content_summary.csv`
- `output/top_10_countries.csv`
- `output/country_type_comparison.csv`
- `output/top_10_countries.png`
- `output/country_type_breakdown.png`
- `reports/country_analysis_results.json`
- `reports/country_analysis_results.js`

## 💡 7. What I Learned
- How to handle multi-valued delimited columns in Pandas using `str.split()` and `explode()`.
- How to filter out missing/placeholder values properly before aggregating statistics.
- How to perform two-variable aggregations using `groupby(["country", "type"]).size().unstack()`.
- How to formulate ethical, accurate data conclusions (e.g. framing as "catalogue titles associated with country" rather than "produced by").
