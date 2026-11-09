// ==============================================================================
// TASK 3: NETFLIX COUNTRY-WISE CONTENT ANALYSIS DASHBOARD
// Frontend Logic: Dynamic table population, Chart.js graphs, and file downloads
// ==============================================================================

document.addEventListener('DOMContentLoaded', () => {

  const defaultData = {
    totalTitles: 8790,
    validTitles: 8503,
    missingTitles: 287,
    totalCountries: 85,
    topCountryName: "United States",
    topCountryCount: 3240,
    top10Countries: [
      { rank: 1, country: "United States", count: 3240 },
      { rank: 2, country: "India", count: 1057 },
      { rank: 3, country: "United Kingdom", count: 638 },
      { rank: 4, country: "Pakistan", count: 421 },
      { rank: 5, country: "Canada", count: 271 },
      { rank: 6, country: "Japan", count: 259 },
      { rank: 7, country: "South Korea", count: 214 },
      { rank: 8, country: "France", count: 213 },
      { rank: 9, country: "Spain", count: 182 },
      { rank: 10, country: "Mexico", count: 138 }
    ],
    countryTypeComparison: [
      { country: "United States", movies: 2395, tvShows: 845, total: 3240 },
      { country: "India", movies: 976, tvShows: 81, total: 1057 },
      { country: "United Kingdom", movies: 387, tvShows: 251, total: 638 },
      { country: "Pakistan", movies: 71, tvShows: 350, total: 421 },
      { country: "Canada", movies: 187, tvShows: 84, total: 271 },
      { country: "Japan", movies: 87, tvShows: 172, total: 259 },
      { country: "South Korea", movies: 49, tvShows: 165, total: 214 },
      { country: "France", movies: 148, tvShows: 65, total: 213 },
      { country: "Spain", movies: 129, tvShows: 53, total: 182 },
      { country: "Mexico", movies: 90, tvShows: 48, total: 138 }
    ],
    businessInsights: [
      "The United States holds the largest volume of Netflix catalogue content (3,240 titles), followed by India (1,057 titles) and the United Kingdom (638 titles).",
      "India is the dominant Asian content contributor with 1,057 titles, consisting predominantly of feature movies over TV shows.",
      "In contrast, countries like South Korea and Japan exhibit a much stronger balance towards TV Shows and anime series, reflecting localized consumption trends.",
      "287 titles (3.27%) lacked verified country metadata ('Not Given') and were excluded from country aggregations to prevent geographical distortion."
    ]
  };

  const results = (typeof COUNTRY_ANALYSIS_RESULTS !== 'undefined') ? COUNTRY_ANALYSIS_RESULTS : defaultData;

  // 1. Populate KPI Cards
  document.getElementById('kpiTotalCountries').textContent = results.totalCountries;
  document.getElementById('kpiValidTitles').textContent = results.validTitles.toLocaleString();
  document.getElementById('kpiTopCountry').textContent = results.topCountryName;
  document.getElementById('kpiTopCount').textContent = results.topCountryCount.toLocaleString() + ' Titles';
  document.getElementById('kpiMissing').textContent = results.missingTitles.toLocaleString();

  // 2. Populate Top 10 Table
  const tableBody = document.getElementById('top10TableBody');
  if (tableBody && results.top10Countries) {
    tableBody.innerHTML = '';
    results.top10Countries.forEach(item => {
      const row = document.createElement('tr');
      const pct = ((item.count / results.validTitles) * 100).toFixed(1);
      row.innerHTML = `
        <td><span class="rank-badge">#${item.rank}</span></td>
        <td><b style="color: #fff;">${item.country}</b></td>
        <td>${item.count.toLocaleString()}</td>
        <td>${pct}%</td>
      `;
      tableBody.appendChild(row);
    });
  }

  // 3. Render Top 10 Horizontal Bar Chart
  const ctxBar = document.getElementById('chartCountries');
  if (ctxBar && results.top10Countries) {
    const labels = results.top10Countries.map(d => d.country);
    const dataVals = results.top10Countries.map(d => d.count);

    new Chart(ctxBar, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Available Titles',
          data: dataVals,
          backgroundColor: '#E50914',
          borderColor: '#FF1E27',
          borderWidth: 1,
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.08)' },
            ticks: { color: '#B3B3B3' }
          },
          y: {
            grid: { display: false },
            ticks: { color: '#FFFFFF', font: { weight: 'bold' } }
          }
        }
      }
    });
  }

  // 4. Render Grouped Movies vs TV Shows Chart
  const ctxType = document.getElementById('chartCountryType');
  if (ctxType && results.countryTypeComparison) {
    const labels = results.countryTypeComparison.map(d => d.country);
    const movies = results.countryTypeComparison.map(d => d.movies);
    const tvShows = results.countryTypeComparison.map(d => d.tvShows);

    new Chart(ctxType, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Movies',
            data: movies,
            backgroundColor: '#E50914',
            borderRadius: 4
          },
          {
            label: 'TV Shows',
            data: tvShows,
            backgroundColor: '#777777',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: { color: '#FFFFFF', font: { weight: 'bold' } }
          }
        },
        scales: {
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.08)' },
            ticks: { color: '#B3B3B3' }
          },
          x: {
            grid: { display: false },
            ticks: { color: '#FFFFFF', maxRotation: 45, minRotation: 45 }
          }
        }
      }
    });
  }

  // 5. Populate Business Insights
  const insightsList = document.getElementById('insightsList');
  if (insightsList && results.businessInsights) {
    insightsList.innerHTML = '';
    results.businessInsights.forEach(txt => {
      const item = document.createElement('div');
      item.className = 'finding-item';
      item.textContent = txt;
      insightsList.appendChild(item);
    });
  }

  // 6. Download Buttons
  document.getElementById('btnDownloadAllCountries').addEventListener('click', () => {
    triggerDownload('output/country_content_summary.csv', 'country_content_summary.csv');
  });

  document.getElementById('btnDownloadTop10').addEventListener('click', () => {
    triggerDownload('output/top_10_countries.csv', 'top_10_countries.csv');
  });

  document.getElementById('btnDownloadTypeComp').addEventListener('click', () => {
    triggerDownload('output/country_type_comparison.csv', 'country_type_comparison.csv');
  });

  function triggerDownload(path, filename) {
    const a = document.createElement('a');
    a.href = path;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
});
