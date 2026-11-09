// ==============================================================================
// TASK 2: NETFLIX CONTENT TYPE ANALYSIS DASHBOARD
// Frontend Logic: Dynamic statistics, Chart.js rendering, and file downloads
// ==============================================================================

document.addEventListener('DOMContentLoaded', () => {

  const defaultData = {
    totalRecords: 8790,
    moviesCount: 6126,
    tvShowsCount: 2664,
    moviePercentage: 69.69,
    tvShowPercentage: 30.31,
    ratio: 2.30,
    keyFindings: [
      "Movies dominate the Netflix streaming catalog, representing 6,126 titles (69.69% of total content).",
      "TV Shows account for 2,664 titles (30.31% of total content).",
      "Movies outnumber TV Shows by a ratio of 2.30 : 1, indicating that Netflix's catalog originated with a heavy emphasis on film acquisition before expanding episodic series."
    ]
  };

  const results = (typeof CONTENT_TYPE_RESULTS !== 'undefined') ? CONTENT_TYPE_RESULTS : defaultData;

  // 1. Populate KPI Cards
  document.getElementById('kpiTotal').textContent = results.totalRecords.toLocaleString();
  document.getElementById('kpiMovies').textContent = results.moviesCount.toLocaleString();
  document.getElementById('kpiTVShows').textContent = results.tvShowsCount.toLocaleString();
  document.getElementById('kpiMoviePct').textContent = results.moviePercentage + '%';
  document.getElementById('kpiTVPct').textContent = results.tvShowPercentage + '%';
  document.getElementById('kpiRatio').textContent = results.ratio + ' : 1';

  // 2. Render Chart.js Bar Chart
  const ctxBar = document.getElementById('chartBar');
  if (ctxBar) {
    new Chart(ctxBar, {
      type: 'bar',
      data: {
        labels: ['Movies', 'TV Shows'],
        datasets: [{
          label: 'Total Titles',
          data: [results.moviesCount, results.tvShowsCount],
          backgroundColor: ['#E50914', '#555555'],
          borderColor: ['#FF1E27', '#777777'],
          borderWidth: 1.5,
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.08)' },
            ticks: { color: '#B3B3B3' }
          },
          x: {
            grid: { display: false },
            ticks: { color: '#FFFFFF', font: { weight: 'bold' } }
          }
        }
      }
    });
  }

  // 3. Render Chart.js Donut / Pie Chart
  const ctxPie = document.getElementById('chartPie');
  if (ctxPie) {
    new Chart(ctxPie, {
      type: 'doughnut',
      data: {
        labels: ['Movies', 'TV Shows'],
        datasets: [{
          data: [results.moviePercentage, results.tvShowPercentage],
          backgroundColor: ['#E50914', '#383838'],
          borderColor: '#141414',
          borderWidth: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: '#FFFFFF', font: { size: 12, weight: 'bold' } }
          }
        },
        cutout: '60%'
      }
    });
  }

  // 4. Populate Key Findings List
  const findingsList = document.getElementById('findingsList');
  if (findingsList && results.keyFindings) {
    findingsList.innerHTML = '';
    results.keyFindings.forEach(f => {
      const item = document.createElement('div');
      item.className = 'finding-item';
      item.textContent = f;
      findingsList.appendChild(item);
    });
  }

  // 5. Download Triggers
  document.getElementById('btnDownloadSummary').addEventListener('click', () => {
    downloadFile('output/content_type_summary.csv', 'content_type_summary.csv');
  });

  document.getElementById('btnDownloadPercentages').addEventListener('click', () => {
    downloadFile('output/content_type_percentages.csv', 'content_type_percentages.csv');
  });

  function downloadFile(path, name) {
    const a = document.createElement('a');
    a.href = path;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
});
