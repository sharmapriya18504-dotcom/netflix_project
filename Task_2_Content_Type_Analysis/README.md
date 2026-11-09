# 🎬 Task 2: Netflix Content Type Analysis Dashboard
### Auspify Data Analysis Using Python Internship — Task 2 (Easy)

## 📌 1. About the Project
This project explores the content distribution of the Netflix catalog, specifically analyzing the proportion and relationship between standalone feature **Movies** and episodic **TV Shows**.

## 🎯 2. Project Objective
- Load and inspect the verified Netflix dataset.
- Calculate the total count and percentage of Movies and TV Shows using Pandas `value_counts()`.
- Compare content proportions and compute the Movie-to-TV Show ratio.
- Generate high-resolution Bar Charts and Pie Charts using Matplotlib.
- Present the results in an interactive, Netflix-inspired dark theme web dashboard.

## 🛠️ 3. Tools & Technologies Used
- **Language**: Python 3.x
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Matplotlib (Python), Chart.js (Web)
- **Frontend Dashboard**: HTML5, CSS3, Vanilla JavaScript

## 🔍 4. Step-by-Step Analysis Workflow
1. **Load Data**: Sourced from `../output/cleaned_netflix_dataset.csv` (8,790 catalog titles).
2. **Calculate Counts**: Evaluated content types using `df["type"].value_counts()`.
   - **Movies**: 6,126 titles (69.69%)
   - **TV Shows**: 2,664 titles (30.31%)
3. **Calculate Ratio**: Movies outnumber TV Shows by `2.30 : 1`.
4. **Generate Visualizations**:
   - `output/content_type_bar_chart.png`: Shows absolute volumes.
   - `output/content_type_pie_chart.png`: Highlights relative percentage shares.
5. **Export Deliverables**: Saved CSV reports and JSON results for dashboard binding.

## 🚀 5. How to Run the Project

### Step 1: Run the Python Analysis
Open terminal inside the `Task_2_Content_Type_Analysis/` folder:
```bash
python analysis.py
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
- `output/content_type_summary.csv`
- `output/content_type_percentages.csv`
- `output/content_type_bar_chart.png`
- `output/content_type_pie_chart.png`
- `reports/analysis_results.json`
- `reports/analysis_results.js`

## 💡 7. What I Learned
- How to use Pandas `value_counts()` and calculate proportion percentages.
- How to export publication-quality dark-themed charts in Matplotlib.
- How to dynamically connect Python data outputs to an interactive HTML/CSS/JavaScript web dashboard.
- Why streaming platforms maintain a balance between quick movie viewings and high-engagement episodic TV shows.
