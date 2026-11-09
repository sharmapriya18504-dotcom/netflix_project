# 🎬 PROJECT 1: Netflix Data Cleaning & Preparation
### Auspify Data Analysis Using Python Internship — Task 1 (Easy)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Cleaning-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![HTML5](https://img.shields.io/badge/HTML5-Modern_UI-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-Netflix_Dark_Theme-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla_ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Status](https://img.shields.io/badge/Internship_Evaluation-Ready-46D369?style=for-the-badge)](https://github.com/sharmapriya18504-dotcom/netflix_project)

---

## 📌 1. Project Objective

The goal of this project is to prepare and organize the real **Netflix streaming catalog** (8,790 rows and 10 columns) for business analytics and reporting using **Python** and **Pandas**.

Following strict data ethics and industry standards:
- **No artificial data generation**: Real dataset characteristics are preserved.
- **Accurate missing value detection**: Standard `isnull().sum()` shows 0, but 2,875 real records have `"Not Given"` placeholders in `director` and `country`. These are converted to standard `NaN` without deleting genuine catalog records.
- **Duplicate verification**: Verified that there are 0 exact duplicates and 0 duplicate `show_id` values (100% data preservation).
- **Standardization**: Text stripped of whitespace, content types standardized (`Movie`, `TV Show`), ratings standardized, and dates converted to ISO `YYYY-MM-DD`.

---

## 📁 2. Project Folder Structure

```text
Netflix_Data_Cleaning/
│
├── data/
│   ├── Dataset(1).csv               # Original raw dataset (8,790 rows, 10 columns)
│   └── Dataset.csv                  # Dataset alias for compatibility
│
├── output/
│   ├── cleaned_netflix_dataset.csv  # Standardized, cleaned dataset ready for analysis
│   ├── missing_values_report.csv    # Column-by-column missing/placeholder metrics
│   └── cleaning_summary.txt         # Executive cleaning summary & audit log
│
├── reports/
│   ├── cleaning_results.json        # Machine-readable cleaning metrics
│   └── cleaning_results.js          # Direct client-side JavaScript result export
│
├── cleaning.py                      # Beginner-friendly procedural Python cleaning script
├── index.html                       # Netflix-inspired interactive project report web UI
├── style.css                        # Cinematic dark theme styling (#141414, #E50914)
├── script.js                        # Dynamic table rendering and CSV download triggers
├── requirements.txt                 # Core dependencies (pandas, numpy, matplotlib)
└── README.md                        # Complete project documentation & viva guide
```

---

## 📊 3. Dataset Characteristics & Cleaning Summary

| Column Name | Raw Data Type | Cleaned Data Type | Actual NaN | "Not Given" Count | Missing % | Action Taken |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `show_id` | object | object | 0 | 0 | 0.00% | Verified 100% unique primary keys |
| `type` | object | object | 0 | 0 | 0.00% | Standardized to 'Movie' & 'TV Show' |
| `title` | object | object | 0 | 0 | 0.00% | Stripped leading/trailing whitespace |
| `director` | object | object | 0 | **2,588** | **29.44%** | Converted `"Not Given"` ➔ `np.nan` (Rows preserved) |
| `country` | object | object | 0 | **287** | **3.27%** | Converted `"Not Given"` ➔ `np.nan` (Rows preserved) |
| `date_added` | object | datetime64[ns] | 0 | 0 | 0.00% | Converted from `M/D/YYYY` to `YYYY-MM-DD` |
| `release_year` | int64 | int64 | 0 | 0 | 0.00% | Verified range: 1925 to 2021 |
| `rating` | object | object | 0 | 0 | 0.00% | Standardized uppercase whitespace |
| `duration` | object | object | 0 | 0 | 0.00% | Preserved duration units (`min`, `Season(s)`) |
| `listed_in` | object | object | 0 | 0 | 0.00% | Stripped text whitespace |

### Key Metrics
- **Initial Catalog Rows**: 8,790
- **Final Cleaned Rows**: 8,790 (100% data retention)
- **Duplicate Rows Found & Removed**: 0
- **Total Missing Placeholders Handled**: 2,875 (`director`: 2,588, `country`: 287)
- **Content Breakdown**: 6,126 Movies (69.69%) and 2,664 TV Shows (30.31%)

---

## 🚀 4. How to Run the Project

### Prerequisites
Make sure Python 3.8+ is installed.

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Cleaning Script
```bash
python cleaning.py
```
*The script will read the raw dataset, run all 5 cleaning steps, display the results in the terminal, and generate all output files in `output/` and `reports/`.*

### Step 3: Open the Web Dashboard
You can open `index.html` in your browser directly:
- **Option A (Direct)**: Double-click `index.html` in File Explorer.
- **Option B (Python Local Server)**:
  ```bash
  python -m http.server 8000
  ```
  Then visit `http://localhost:8000` in your browser.

---

## 🎨 5. Web Dashboard Highlights

The frontend (`index.html`) is designed with a **Netflix Cinematic Dark UI**:
- **Palette**: Deep Black (`#141414`), Netflix Red (`#E50914`), Card Surface (`#1C1C1C`), and Crisp White (`#FFFFFF`).
- **Dynamic KPI Cards**: Displays real rows, columns, placeholder counts, and duplicates dynamically populated from `cleaning_results.js`.
- **5-Step Workflow Tracker**: Visual completion badges for each cleaning step.
- **Data Quality Report Table**: Features visual percentage progress bars for missing values.
- **Before & After Record Comparison**: Inspects sample records side-by-side to highlight whitespace and date standardization.
- **Download Center**: One-click download buttons for:
  - `cleaned_netflix_dataset.csv`
  - `missing_values_report.csv`
  - `cleaning_summary.txt`
- **Internship Evaluation & Viva Guide**: Curated questions and student-friendly answers for project presentation.

---

## 🎓 6. Internship Viva Q&A (Quick Reference)

### Q1: Why did `df.isnull().sum()` show 0 missing values initially?
**Answer**: Because the dataset creator used the text string `"Not Given"` instead of empty cells or standard `NaN`. Python string functions treat `"Not Given"` as a valid string. We identified this by inspecting distinct text values and replaced `"Not Given"` with `np.nan`.

### Q2: Why didn't you drop rows with missing director or country?
**Answer**: Dropping them would remove 2,588 titles (over 29% of the dataset!). The missing director does not affect the title, release year, genre, or duration. Dropping rows unnecessarily creates severe selection bias.

### Q3: How did you verify duplicates?
**Answer**: We checked both whole-row duplicates using `df.duplicated().sum()` (which returned 0) and primary key uniqueness using `df['show_id'].duplicated().sum()` (which returned 0). All 8,790 records are distinct.

### Q4: Why convert `date_added` into a `datetime` format?
**Answer**: In the raw dataset, dates are stored as raw strings (e.g., `9/25/2021`). Converting them with `pd.to_datetime()` enables sorting chronologically, time-series analysis, and extracting release month/year easily in Pandas or visualization tools.

---

## 👩‍💻 Author & Acknowledgements
- **Author**: Priya Sharma
- **Role**: Data Analytics Intern
- **Program**: Auspify Data Analysis Using Python Internship (Task 1 — Easy)
- **License**: MIT
