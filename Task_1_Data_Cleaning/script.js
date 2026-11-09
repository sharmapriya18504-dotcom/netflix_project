// ==============================================================================
// PROJECT 1: NETFLIX DATA CLEANING & PREPARATION
// Auspify Data Analysis Internship - Task 1 (Easy)
// Frontend Logic: Dynamic rendering, data table injection, and file downloads
// ==============================================================================

document.addEventListener('DOMContentLoaded', () => {

  // Default fallback data (sourced directly from actual Python cleaning.py execution)
  const defaultData = {
    projectName: "Netflix Data Cleaning & Preparation",
    taskName: "Task 1 (Easy) – Auspify Data Analysis Internship",
    author: "Priya Sharma",
    datasetSource: "data/Dataset(1).csv",
    originalRows: 8790,
    originalCols: 10,
    cleanedRows: 8790,
    cleanedCols: 10,
    exactDuplicates: 0,
    duplicateShowIds: 0,
    actualNanTotal: 0,
    notGivenDirector: 2588,
    notGivenCountry: 287,
    totalNotGiven: 2875,
    moviesCount: 6126,
    tvShowsCount: 2664,
    invalidDates: 0,
    dateMin: "2008-01-01",
    dateMax: "2021-09-25",
    missingReport: [
      { column_name: "show_id", actual_nan_count: 0, not_given_count: 0, total_missing_count: 0, missing_percentage: 0.0, data_type: "object" },
      { column_name: "type", actual_nan_count: 0, not_given_count: 0, total_missing_count: 0, missing_percentage: 0.0, data_type: "object" },
      { column_name: "title", actual_nan_count: 0, not_given_count: 0, total_missing_count: 0, missing_percentage: 0.0, data_type: "object" },
      { column_name: "director", actual_nan_count: 0, not_given_count: 2588, total_missing_count: 2588, missing_percentage: 29.44, data_type: "object" },
      { column_name: "country", actual_nan_count: 0, not_given_count: 287, total_missing_count: 287, missing_percentage: 3.27, data_type: "object" },
      { column_name: "date_added", actual_nan_count: 0, not_given_count: 0, total_missing_count: 0, missing_percentage: 0.0, data_type: "datetime64[ns]" },
      { column_name: "release_year", actual_nan_count: 0, not_given_count: 0, total_missing_count: 0, missing_percentage: 0.0, data_type: "int64" },
      { column_name: "rating", actual_nan_count: 0, not_given_count: 0, total_missing_count: 0, missing_percentage: 0.0, data_type: "object" },
      { column_name: "duration", actual_nan_count: 0, not_given_count: 0, total_missing_count: 0, missing_percentage: 0.0, data_type: "object" },
      { column_name: "listed_in", actual_nan_count: 0, not_given_count: 0, total_missing_count: 0, missing_percentage: 0.0, data_type: "object" }
    ],
    sampleOriginal: [
      { show_id: "s1", type: "Movie", title: "Dick Johnson Is Dead", director: "Kirsten Johnson", country: "United States", date_added: "9/25/2021", release_year: 2020, rating: "PG-13", duration: "90 min", listed_in: "Documentaries" },
      { show_id: "s3", type: "TV Show", title: "Ganglands", director: "Julien Leclercq", country: "France", date_added: "9/24/2021", release_year: 2021, rating: "TV-MA", duration: "1 Season", listed_in: "Crime TV Shows, International TV Shows" },
      { show_id: "s6", type: "TV Show", title: "Midnight Mass", director: "Mike Flanagan", country: "United States", date_added: "9/24/2021", release_year: 2021, rating: "TV-MA", duration: "1 Season", listed_in: "TV Dramas, TV Horror, TV Mysteries" },
      { show_id: "s14", type: "Movie", title: "Confessions of an Invisible Girl", director: "Bruno Garotti", country: "Brazil", date_added: "9/22/2021", release_year: 2021, rating: "TV-PG", duration: "91 min", listed_in: "Children & Family Movies, Comedies" },
      { show_id: "s8", type: "Movie", title: "Sankofa", director: "Haile Gerima", country: "United States", date_added: "9/24/2021", release_year: 1993, rating: "TV-MA", duration: "125 min", listed_in: "Dramas, Independent Movies" }
    ],
    sampleCleaned: [
      { show_id: "s1", type: "Movie", title: "Dick Johnson Is Dead", director: "Kirsten Johnson", country: "United States", date_added: "2021-09-25", release_year: 2020, rating: "PG-13", duration: "90 min", listed_in: "Documentaries" },
      { show_id: "s3", type: "TV Show", title: "Ganglands", director: "Julien Leclercq", country: "France", date_added: "2021-09-24", release_year: 2021, rating: "TV-MA", duration: "1 Season", listed_in: "Crime TV Shows, International TV Shows" },
      { show_id: "s6", type: "TV Show", title: "Midnight Mass", director: "Mike Flanagan", country: "United States", date_added: "2021-09-24", release_year: 2021, rating: "TV-MA", duration: "1 Season", listed_in: "TV Dramas, TV Horror, TV Mysteries" },
      { show_id: "s14", type: "Movie", title: "Confessions of an Invisible Girl", director: "Bruno Garotti", country: "Brazil", date_added: "2021-09-22", release_year: 2021, rating: "TV-PG", duration: "91 min", listed_in: "Children & Family Movies, Comedies" },
      { show_id: "s8", type: "Movie", title: "Sankofa", director: "Haile Gerima", country: "United States", date_added: "2021-09-24", release_year: 1993, rating: "TV-MA", duration: "125 min", listed_in: "Dramas, Independent Movies" }
    ]
  };

  // Determine active dataset (Check window.CLEANING_RESULTS from reports/cleaning_results.js first)
  const results = (typeof CLEANING_RESULTS !== 'undefined') ? CLEANING_RESULTS : defaultData;

  // 1. Populate KPI Overview Cards
  document.getElementById('kpiTotalRows').textContent = results.cleanedRows.toLocaleString();
  document.getElementById('kpiTotalCols').textContent = results.cleanedCols;
  document.getElementById('kpiMissingTotal').textContent = results.totalNotGiven.toLocaleString();
  document.getElementById('kpiExactDuplicates').textContent = results.exactDuplicates;
  document.getElementById('kpiMoviesCount').textContent = results.moviesCount.toLocaleString();
  document.getElementById('kpiTVCount').textContent = results.tvShowsCount.toLocaleString();

  // 2. Render Data Quality Table
  const tableBody = document.getElementById('qualityTableBody');
  if (tableBody && results.missingReport) {
    tableBody.innerHTML = '';
    results.missingReport.forEach(item => {
      const row = document.createElement('tr');
      const hasPlaceholders = item.not_given_count > 0;
      const statusHtml = hasPlaceholders
        ? `<span class="status-placeholder">⚠️ ${item.not_given_count.toLocaleString()} ('Not Given' ➔ NaN)</span>`
        : `<span class="status-clean">✓ 100% Complete</span>`;

      row.innerHTML = `
        <td><span class="col-badge">${item.column_name}</span></td>
        <td><code>${item.data_type}</code></td>
        <td>${item.actual_nan_count}</td>
        <td>${item.not_given_count.toLocaleString()}</td>
        <td>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: ${item.missing_percentage}%;"></div>
          </div>
          <span>${item.missing_percentage}%</span>
        </td>
        <td>${statusHtml}</td>
      `;
      tableBody.appendChild(row);
    });
  }

  // 3. Render Sample Comparison Tables
  renderSampleTable('tableOriginal', results.sampleOriginal);
  renderSampleTable('tableCleaned', results.sampleCleaned);

  function renderSampleTable(elemId, dataList) {
    const tableElem = document.getElementById(elemId);
    if (!tableElem || !dataList || dataList.length === 0) return;

    let html = `<thead><tr>
      <th>show_id</th>
      <th>type</th>
      <th>title</th>
      <th>director</th>
      <th>country</th>
      <th>date_added</th>
      <th>release_year</th>
      <th>rating</th>
      <th>duration</th>
    </tr></thead><tbody>`;

    dataList.forEach(item => {
      html += `<tr>
        <td><b>${item.show_id}</b></td>
        <td>${item.type}</td>
        <td>${item.title}</td>
        <td>${item.director || '<i style="color:#888;">NaN</i>'}</td>
        <td>${item.country || '<i style="color:#888;">NaN</i>'}</td>
        <td>${item.date_added}</td>
        <td>${item.release_year}</td>
        <td>${item.rating}</td>
        <td>${item.duration}</td>
      </tr>`;
    });

    html += `</tbody>`;
    tableElem.innerHTML = html;
  }

  // 4. Download Functionality
  document.getElementById('btnDownloadCleaned').addEventListener('click', () => {
    triggerFileDownload('output/cleaned_netflix_dataset.csv', 'cleaned_netflix_dataset.csv');
  });

  document.getElementById('btnDownloadReport').addEventListener('click', () => {
    triggerFileDownload('output/missing_values_report.csv', 'missing_values_report.csv');
  });

  document.getElementById('btnDownloadSummary').addEventListener('click', () => {
    triggerFileDownload('output/cleaning_summary.txt', 'cleaning_summary.txt');
  });

  function triggerFileDownload(filePath, fileName) {
    const a = document.createElement('a');
    a.href = filePath;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  // 5. Sticky Navigation Highlighting & Smooth Scrolling
  const navBtns = document.querySelectorAll('.nav-btn');
  navBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      navBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const targetId = btn.getAttribute('data-target');
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  window.addEventListener('scroll', () => {
    const sections = ['overview', 'dataset', 'workflow', 'quality', 'comparison', 'downloads', 'viva'];
    const scrollPos = window.scrollY + 100;

    sections.forEach(secId => {
      const el = document.getElementById(secId);
      if (el) {
        const top = el.offsetTop;
        const height = el.offsetHeight;
        if (scrollPos >= top && scrollPos < top + height) {
          navBtns.forEach(b => {
            if (b.getAttribute('data-target') === secId) {
              b.classList.add('active');
            } else {
              b.classList.remove('active');
            }
          });
        }
      }
    });
  });
});
