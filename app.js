// ==============================================================================
// NETFLIX ANALYTICS - APPLICATION LOGIC
// Client-side execution, Chart.js initialization, live search, and modal handler
// ==============================================================================

document.addEventListener('DOMContentLoaded', () => {
  // Check if dataset is loaded
  if (typeof NETFLIX_METRICS === 'undefined' || typeof NETFLIX_TITLES === 'undefined') {
    console.error('Data not loaded. Please ensure data.js is included.');
    return;
  }

  // ============================================================================
  // CURATED CINEMATIC POSTER IMAGE MAP (HIGH-RESOLUTION UNSPLASH STILLS)
  // ============================================================================
  const POSTER_COLLECTION = {
    action: [
      'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80'
    ],
    comedy: [
      'https://images.unsplash.com/photo-1514306191717-452ec28c7814?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1585647347483-22b66260dfff?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?w=600&auto=format&fit=crop&q=80'
    ],
    drama: [
      'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?w=600&auto=format&fit=crop&q=80'
    ],
    documentary: [
      'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=600&auto=format&fit=crop&q=80'
    ],
    horror: [
      'https://images.unsplash.com/photo-1509248961158-e54f6934749c?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80'
    ],
    romance: [
      'https://images.unsplash.com/photo-1518895949257-7621c3c786d7?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=600&auto=format&fit=crop&q=80'
    ],
    kids: [
      'https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1563089145-599997674d42?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=600&auto=format&fit=crop&q=80'
    ],
    scifi: [
      'https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&auto=format&fit=crop&q=80'
    ],
    international: [
      'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&auto=format&fit=crop&q=80'
    ],
    default: [
      'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=600&auto=format&fit=crop&q=80'
    ]
  };

  // Specific high-profile poster mapping for iconic dataset titles
  const SPECIAL_TITLES_MAP = {
    'Stranger Things': 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80',
    'Squid Game': 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=600&auto=format&fit=crop&q=80',
    'The Crown': 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=600&auto=format&fit=crop&q=80',
    'Sacred Games': 'https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&auto=format&fit=crop&q=80',
    'Our Planet': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&auto=format&fit=crop&q=80'
  };

  // Deterministic poster resolver
  function getPosterImage(item) {
    if (!item) return POSTER_COLLECTION.default[0];

    // Check special exact title map first
    if (SPECIAL_TITLES_MAP[item.title]) {
      return SPECIAL_TITLES_MAP[item.title];
    }

    // Determine category based on listed_in / country
    const genre = (item.listed_in || '').toLowerCase();
    const country = (item.country || '').toLowerCase();
    let category = 'default';

    if (genre.includes('horror') || genre.includes('thriller')) {
      category = 'horror';
    } else if (genre.includes('sci-fi') || genre.includes('fantasy')) {
      category = 'scifi';
    } else if (genre.includes('action') || genre.includes('adventure')) {
      category = 'action';
    } else if (genre.includes('comedy') || genre.includes('comedi')) {
      category = 'comedy';
    } else if (genre.includes('documentar') || genre.includes('docuseries') || genre.includes('nature')) {
      category = 'documentary';
    } else if (genre.includes('children') || genre.includes('kids') || genre.includes('family') || genre.includes('anime')) {
      category = 'kids';
    } else if (genre.includes('romance') || genre.includes('romantic')) {
      category = 'romance';
    } else if (country.includes('india') || genre.includes('international') || country.includes('japan') || country.includes('korea')) {
      category = 'international';
    } else if (genre.includes('drama')) {
      category = 'drama';
    }

    // Use a numeric hash of show_id to pick deterministically among the category images
    const list = POSTER_COLLECTION[category] || POSTER_COLLECTION.default;
    let hash = 0;
    const str = item.show_id || item.title || '0';
    for (let i = 0; i < str.length; i++) {
      hash = (hash * 31 + str.charCodeAt(i)) % list.length;
    }
    return list[Math.abs(hash)];
  }

  // State Management
  let currentFilteredTitles = [...NETFLIX_TITLES];
  let currentPage = 1;
  const itemsPerPage = 12;
  let currentTypeFilter = 'All';
  let currentSearchQuery = '';
  let currentSort = 'newest';

  // 1. Initialize Hero Section
  initHeroBanner();

  // 2. Initialize KPI Cards
  initKPICards();

  // 3. Initialize Acclaimed Spotlights Row
  initSpotlights();

  // 4. Initialize Interactive Chart.js Visualizations
  initCharts();

  // 5. Initialize Catalog Explorer & Search
  initCatalogControls();
  renderCatalogPage(1);

  // 6. Initialize Movie Modal
  initModal();

  // 7. Navigation Smooth Scrolling & Active State
  initNavigation();

  // 8. CSV Export Button
  initExport();

  // 9. Floating Back To Top Button
  initBackToTop();

  // ============================================================================
  // HERO BANNER
  // ============================================================================
  function initHeroBanner() {
    // Pick Stranger Things or standout title
    const featured = NETFLIX_TITLES.find(t => t.title.toLowerCase() === 'stranger things') ||
                     NETFLIX_TITLES.find(t => t.title.toLowerCase().includes('queen') || t.title.toLowerCase().includes('dead')) ||
                     NETFLIX_TITLES[0];

    document.getElementById('heroTitle').textContent = featured.title;
    document.getElementById('heroType').textContent = featured.type.toUpperCase();
    document.getElementById('heroYear').textContent = featured.release_year;
    document.getElementById('heroRating').textContent = featured.rating;
    document.getElementById('heroDuration').textContent = featured.duration;
    document.getElementById('heroCountry').textContent = featured.country || 'Global';
    document.getElementById('heroGenre').textContent = featured.listed_in;
    document.getElementById('heroDesc').textContent = `Explore verified metadata for "${featured.title}", produced in ${featured.country || 'various countries'} and categorized under ${featured.listed_in}.`;

    // Right poster card
    const heroImg = document.getElementById('heroPosterImg');
    const heroPosterTitle = document.getElementById('heroPosterTitle');
    const heroPosterMeta = document.getElementById('heroPosterMeta');
    const heroCard = document.getElementById('heroPosterCard');

    if (heroImg) heroImg.src = getPosterImage(featured);
    if (heroPosterTitle) heroPosterTitle.textContent = featured.title;
    if (heroPosterMeta) heroPosterMeta.textContent = `${featured.release_year} • ${featured.country || 'Global'}`;

    if (heroCard) {
      heroCard.addEventListener('click', () => openModal(featured));
    }

    document.getElementById('btnHeroDetails').addEventListener('click', () => {
      openModal(featured);
    });
  }

  // ============================================================================
  // KPI CARDS
  // ============================================================================
  function initKPICards() {
    document.getElementById('kpiTotalTitles').textContent = NETFLIX_METRICS.totalTitles.toLocaleString();
    document.getElementById('kpiMoviesCount').textContent = NETFLIX_METRICS.moviesCount.toLocaleString();
    document.getElementById('kpiTVCount').textContent = NETFLIX_METRICS.tvCount.toLocaleString();
    document.getElementById('kpiCountries').textContent = NETFLIX_METRICS.totalCountries.toLocaleString();
    document.getElementById('kpiTopGenre').textContent = NETFLIX_METRICS.topGenreName;
    document.getElementById('kpiPeakYear').textContent = `${NETFLIX_METRICS.peakYear} (${NETFLIX_METRICS.peakYearCount.toLocaleString()})`;
  }

  // ============================================================================
  // ACCLAIMED SPOTLIGHTS ROW
  // ============================================================================
  function initSpotlights() {
    const spotlightContainer = document.getElementById('spotlightGrid');
    if (!spotlightContainer) return;

    // Target 5 iconic dataset titles
    const targetTitles = ['Squid Game', 'Stranger Things', 'The Crown', 'Sacred Games', 'Our Planet'];
    const spotlights = [];

    targetTitles.forEach(tName => {
      const match = NETFLIX_TITLES.find(t => t.title.toLowerCase() === tName.toLowerCase());
      if (match) spotlights.push(match);
    });

    // If any couldn't be matched, fill with top titles
    if (spotlights.length < 5) {
      NETFLIX_TITLES.slice(0, 5 - spotlights.length).forEach(t => spotlights.push(t));
    }

    spotlightContainer.innerHTML = '';

    spotlights.forEach((item, index) => {
      const card = document.createElement('div');
      card.className = 'spotlight-card';
      const poster = getPosterImage(item);

      card.innerHTML = `
        <div class="spotlight-poster">
          <img src="${poster}" loading="lazy" alt="${item.title}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=600&auto=format&fit=crop&q=80';" />
          <div class="spotlight-poster-gradient"></div>
          <span class="spotlight-rank-badge">★ TOP PICK #${index + 1}</span>
          <span class="spotlight-country-badge">${item.country ? item.country.split(',')[0].trim() : 'Global'}</span>
        </div>
        <div class="spotlight-body">
          <h4 class="spotlight-title">${item.title}</h4>
          <div class="spotlight-meta">
            <span>📅 ${item.release_year}</span>
            <span class="rating-badge" style="font-size: 10px; padding: 1px 6px;">${item.rating}</span>
            <span>⏱️ ${item.duration}</span>
          </div>
          <p class="spotlight-genre">🎭 ${item.listed_in}</p>
          <button class="card-btn">▶ View Metadata</button>
        </div>
      `;

      card.addEventListener('click', () => {
        openModal(item);
      });

      spotlightContainer.appendChild(card);
    });
  }

  // ============================================================================
  // CHART.JS INITIALIZATION
  // ============================================================================
  function initCharts() {
    // Global Chart.js defaults for Netflix Dark Theme
    Chart.defaults.color = '#B3B3B3';
    Chart.defaults.font.family = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";

    // Common Tooltip Styling
    const darkTooltip = {
      backgroundColor: 'rgba(15, 15, 15, 0.95)',
      titleColor: '#FFFFFF',
      bodyColor: '#D1D1D1',
      borderColor: '#E50914',
      borderWidth: 1,
      padding: 12,
      cornerRadius: 6,
      boxPadding: 4,
      usePointStyle: true
    };

    // Chart 1: Donut Chart (Movies vs TV Shows)
    const ctxType = document.getElementById('chartContentType').getContext('2d');
    new Chart(ctxType, {
      type: 'doughnut',
      data: {
        labels: ['Movies (69.7%)', 'TV Shows (30.3%)'],
        datasets: [{
          data: [NETFLIX_METRICS.moviesCount, NETFLIX_METRICS.tvCount],
          backgroundColor: ['#E50914', '#2E2E2E'],
          borderColor: '#141414',
          borderWidth: 3,
          hoverBackgroundColor: ['#FF1E27', '#404040'],
          hoverOffset: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 14,
              padding: 18,
              font: { family: "'Outfit', sans-serif", weight: '600', size: 13 }
            }
          },
          tooltip: darkTooltip
        },
        cutout: '66%'
      }
    });

    // Chart 2: Top 10 Countries Bar Chart
    const ctxCountries = document.getElementById('chartTopCountries').getContext('2d');
    const countryLabels = NETFLIX_METRICS.topCountriesLabels || Object.keys(NETFLIX_METRICS.topCountries || {});
    const countryValues = NETFLIX_METRICS.topCountriesValues || Object.values(NETFLIX_METRICS.topCountries || {});

    new Chart(ctxCountries, {
      type: 'bar',
      data: {
        labels: countryLabels,
        datasets: [{
          label: 'Total Titles',
          data: countryValues,
          backgroundColor: '#E50914',
          hoverBackgroundColor: '#FF2A33',
          borderRadius: 4,
          maxBarThickness: 24
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: darkTooltip
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#888' }
          },
          y: {
            grid: { display: false },
            ticks: {
              color: '#DDD',
              font: { family: "'Outfit', sans-serif", weight: '700', size: 12 }
            }
          }
        }
      }
    });

    // Chart 3: Historical Release Year Trend (Area Line Chart)
    const ctxYears = document.getElementById('chartReleaseYear').getContext('2d');
    const gradientFill = ctxYears.createLinearGradient(0, 0, 0, 320);
    gradientFill.addColorStop(0, 'rgba(229, 9, 20, 0.45)');
    gradientFill.addColorStop(1, 'rgba(229, 9, 20, 0.0)');

    const yearLabels = NETFLIX_METRICS.releaseYearsLabels || Object.keys(NETFLIX_METRICS.releaseYears || {});
    const yearValues = NETFLIX_METRICS.releaseYearsValues || Object.values(NETFLIX_METRICS.releaseYears || {});

    new Chart(ctxYears, {
      type: 'line',
      data: {
        labels: yearLabels,
        datasets: [{
          label: 'Titles Released',
          data: yearValues,
          borderColor: '#E50914',
          borderWidth: 2.8,
          backgroundColor: gradientFill,
          fill: true,
          tension: 0.35,
          pointRadius: 2.5,
          pointHoverRadius: 7,
          pointHoverBackgroundColor: '#FFFFFF',
          pointHoverBorderColor: '#E50914',
          pointHoverBorderWidth: 2.5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: darkTooltip
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.04)' },
            ticks: {
              color: '#AAA',
              maxTicksLimit: 16,
              font: { family: "'Inter', sans-serif", weight: '600' }
            }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.06)' },
            ticks: { color: '#888' }
          }
        }
      }
    });

    // Chart 4: Top 10 Genres Horizontal Bar Chart
    const ctxGenres = document.getElementById('chartTopGenres').getContext('2d');
    const genreLabels = NETFLIX_METRICS.topGenresLabels || Object.keys(NETFLIX_METRICS.topGenres || {});
    const genreValues = NETFLIX_METRICS.topGenresValues || Object.values(NETFLIX_METRICS.topGenres || {});

    new Chart(ctxGenres, {
      type: 'bar',
      data: {
        labels: genreLabels,
        datasets: [{
          label: 'Titles Count',
          data: genreValues,
          backgroundColor: '#991117',
          hoverBackgroundColor: '#E50914',
          borderRadius: 4,
          maxBarThickness: 22
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: darkTooltip
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { color: '#888' }
          },
          y: {
            grid: { display: false },
            ticks: {
              color: '#DDD',
              font: { family: "'Outfit', sans-serif", weight: '700', size: 12 }
            }
          }
        }
      }
    });

    // Chart 5: Content Rating Distribution
    const ctxRatings = document.getElementById('chartRatings').getContext('2d');
    const ratingLabels = NETFLIX_METRICS.ratingsLabels || Object.keys(NETFLIX_METRICS.topRatings || {});
    const ratingValues = NETFLIX_METRICS.ratingsValues || Object.values(NETFLIX_METRICS.topRatings || {});

    new Chart(ctxRatings, {
      type: 'bar',
      data: {
        labels: ratingLabels,
        datasets: [{
          label: 'Titles Count',
          data: ratingValues,
          backgroundColor: '#E50914',
          hoverBackgroundColor: '#FF2A33',
          borderRadius: 4,
          maxBarThickness: 28
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: darkTooltip
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: {
              color: '#DDD',
              font: { family: "'Outfit', sans-serif", weight: '700', size: 11.5 }
            }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.06)' },
            ticks: { color: '#888' }
          }
        }
      }
    });

    // Chart 6: Comparative Rating Analysis Across Content Types (Task 5 Step 3)
    const ctxRatingsByType = document.getElementById('chartRatingsByType').getContext('2d');
    const rData = NETFLIX_METRICS.ratingsByType || {
      labels: ['TV-MA', 'TV-14', 'TV-PG', 'R', 'PG-13', 'TV-Y7', 'TV-Y', 'PG'],
      movies: [2062, 1427, 540, 797, 490, 139, 131, 287],
      tvShows: [1143, 730, 321, 2, 0, 194, 175, 0]
    };

    new Chart(ctxRatingsByType, {
      type: 'bar',
      data: {
        labels: rData.labels,
        datasets: [
          {
            label: 'Movies',
            data: rData.movies,
            backgroundColor: '#E50914',
            hoverBackgroundColor: '#FF2A33',
            borderRadius: 4,
            maxBarThickness: 24
          },
          {
            label: 'TV Shows',
            data: rData.tvShows,
            backgroundColor: '#383838',
            hoverBackgroundColor: '#555555',
            borderRadius: 4,
            maxBarThickness: 24
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              boxWidth: 14,
              padding: 16,
              color: '#FFF',
              font: { family: "'Outfit', sans-serif", weight: '700', size: 12 }
            }
          },
          tooltip: darkTooltip
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: {
              color: '#DDD',
              font: { family: "'Outfit', sans-serif", weight: '600', size: 12 }
            }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.06)' },
            ticks: { color: '#888' }
          }
        }
      }
    });
  }

  // ============================================================================
  // CATALOG EXPLORER, SEARCH & FILTER LOGIC
  // ============================================================================
  function initCatalogControls() {
    const searchInput = document.getElementById('catalogSearch');
    const typePills = document.querySelectorAll('.pill-btn');
    const sortSelect = document.getElementById('catalogSort');

    // Live Instant Search
    searchInput.addEventListener('input', (e) => {
      currentSearchQuery = e.target.value.toLowerCase().trim();
      applyFilters();
    });

    // Type Pills (All, Movies, TV Shows)
    typePills.forEach(pill => {
      pill.addEventListener('click', () => {
        typePills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        currentTypeFilter = pill.getAttribute('data-type');
        applyFilters();
      });
    });

    // Sort Dropdown
    sortSelect.addEventListener('change', (e) => {
      currentSort = e.target.value;
      applyFilters();
    });

    // Pagination Controls
    document.getElementById('prevPageBtn').addEventListener('click', () => {
      if (currentPage > 1) {
        currentPage--;
        renderCatalogPage(currentPage);
        document.getElementById('catalog').scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });

    document.getElementById('nextPageBtn').addEventListener('click', () => {
      const maxPages = Math.ceil(currentFilteredTitles.length / itemsPerPage);
      if (currentPage < maxPages) {
        currentPage++;
        renderCatalogPage(currentPage);
        document.getElementById('catalog').scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  function applyFilters() {
    currentFilteredTitles = NETFLIX_TITLES.filter(item => {
      // Type filter
      if (currentTypeFilter !== 'All' && item.type !== currentTypeFilter) {
        return false;
      }

      // Search filter (title, director, country, listed_in)
      if (currentSearchQuery) {
        const titleMatch = (item.title || '').toLowerCase().includes(currentSearchQuery);
        const directorMatch = (item.director || '').toLowerCase().includes(currentSearchQuery);
        const countryMatch = (item.country || '').toLowerCase().includes(currentSearchQuery);
        const genreMatch = (item.listed_in || '').toLowerCase().includes(currentSearchQuery);
        return titleMatch || directorMatch || countryMatch || genreMatch;
      }

      return true;
    });

    // Sorting
    if (currentSort === 'newest') {
      currentFilteredTitles.sort((a, b) => b.release_year - a.release_year);
    } else if (currentSort === 'oldest') {
      currentFilteredTitles.sort((a, b) => a.release_year - b.release_year);
    } else if (currentSort === 'alpha') {
      currentFilteredTitles.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
    }

    currentPage = 1;
    renderCatalogPage(1);
  }

  function renderCatalogPage(page) {
    const grid = document.getElementById('movieGrid');
    grid.innerHTML = '';

    const totalMatches = currentFilteredTitles.length;
    const maxPages = Math.max(1, Math.ceil(totalMatches / itemsPerPage));
    const startIndex = (page - 1) * itemsPerPage;
    const pageItems = currentFilteredTitles.slice(startIndex, startIndex + itemsPerPage);

    // Update Counter & Pagination Info
    document.getElementById('matchesCount').textContent = `Showing ${pageItems.length > 0 ? startIndex + 1 : 0}–${Math.min(startIndex + pageItems.length, totalMatches)} of ${totalMatches.toLocaleString()} matching titles`;
    document.getElementById('pageInfo').textContent = `Page ${page} of ${maxPages.toLocaleString()}`;
    document.getElementById('prevPageBtn').disabled = (page === 1);
    document.getElementById('nextPageBtn').disabled = (page >= maxPages);

    if (pageItems.length === 0) {
      grid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 50px 20px; color: #888;">
          <h3 style="color: #bbb; margin-bottom: 8px; font-family: var(--font-heading);">No matching titles found</h3>
          <p style="font-size: 13.5px;">Try searching for another keyword or switching the content filter.</p>
        </div>
      `;
      return;
    }

    pageItems.forEach(item => {
      const card = document.createElement('div');
      card.className = 'movie-card';
      const posterUrl = getPosterImage(item);

      card.innerHTML = `
        <div class="card-poster">
          <img src="${posterUrl}" loading="lazy" alt="${item.title}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=600&auto=format&fit=crop&q=80';" />
          <div class="poster-gradient"></div>
          <div class="play-overlay">▶</div>
          <span class="type-tag">${item.type}</span>
          <span class="rating-tag-card">${item.rating}</span>
        </div>
        <div class="card-body">
          <h4 class="card-title" title="${item.title}">${item.title}</h4>
          <div class="card-meta">
            <span>📅 ${item.release_year}</span>
            <span>⏱️ ${item.duration}</span>
          </div>
          <p class="card-genre">🎭 ${item.listed_in}</p>
          <button class="card-btn">▶ View Details</button>
        </div>
      `;

      card.addEventListener('click', () => {
        openModal(item);
      });

      grid.appendChild(card);
    });
  }

  // ============================================================================
  // MOVIE MODAL POPUP
  // ============================================================================
  function initModal() {
    const modal = document.getElementById('movieModal');
    const closeBtn = document.getElementById('modalCloseBtn');

    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
      }
    });
  }

  function openModal(item) {
    const modal = document.getElementById('movieModal');
    const posterUrl = getPosterImage(item);

    const modalImg = document.getElementById('modalHeroImg');
    if (modalImg) modalImg.src = posterUrl;

    document.getElementById('modalTitle').textContent = item.title;
    document.getElementById('modalType').textContent = item.type.toUpperCase();
    document.getElementById('modalYear').textContent = item.release_year;
    document.getElementById('modalRating').textContent = item.rating;
    document.getElementById('modalDuration').textContent = item.duration;
    document.getElementById('modalDirector').textContent = item.director || 'Not Given';
    document.getElementById('modalCountry').textContent = item.country || 'Not Given';

    // Genre pills with click-to-filter capability
    const genreContainer = document.getElementById('modalGenres');
    genreContainer.innerHTML = '';
    const genres = (item.listed_in || '').split(',').map(g => g.trim()).filter(Boolean);

    genres.forEach(g => {
      const pill = document.createElement('span');
      pill.className = 'genre-pill';
      pill.textContent = g;
      pill.title = `Click to filter catalog by "${g}"`;
      pill.style.cursor = 'pointer';

      pill.addEventListener('click', () => {
        closeModal();
        const searchInput = document.getElementById('catalogSearch');
        if (searchInput) {
          searchInput.value = g;
          currentSearchQuery = g.toLowerCase();
          applyFilters();
          document.getElementById('catalog').scrollIntoView({ behavior: 'smooth' });
        }
      });

      genreContainer.appendChild(pill);
    });

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    const modal = document.getElementById('movieModal');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
  }

  // ============================================================================
  // NAVIGATION & SCROLL TRACKING
  // ============================================================================
  function initNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        navButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const targetId = btn.getAttribute('data-target');
        const targetElem = document.getElementById(targetId);
        if (targetElem) {
          targetElem.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });

    // Active state highlighting on scroll
    window.addEventListener('scroll', () => {
      const sections = ['overview', 'spotlight', 'charts', 'catalog', 'insights', 'viva'];
      const scrollPos = window.scrollY + 120;

      sections.forEach(id => {
        const sec = document.getElementById(id);
        if (sec) {
          const top = sec.offsetTop;
          const height = sec.offsetHeight;
          if (scrollPos >= top && scrollPos < top + height) {
            navButtons.forEach(b => {
              if (b.getAttribute('data-target') === id) {
                b.classList.add('active');
              } else {
                b.classList.remove('active');
              }
            });
          }
        }
      });
    });
  }

  // ============================================================================
  // CSV EXPORT FUNCTIONALITY
  // ============================================================================
  function initExport() {
    const exportBtn = document.getElementById('btnExportCSV');
    exportBtn.addEventListener('click', () => {
      const headers = ['show_id', 'type', 'title', 'director', 'country', 'release_year', 'rating', 'duration', 'listed_in'];
      let csvContent = 'data:text/csv;charset=utf-8,' + headers.join(',') + '\n';

      NETFLIX_TITLES.forEach(item => {
        const row = [
          item.show_id,
          `"${(item.type || '').replace(/"/g, '""')}"`,
          `"${(item.title || '').replace(/"/g, '""')}"`,
          `"${(item.director || '').replace(/"/g, '""')}"`,
          `"${(item.country || '').replace(/"/g, '""')}"`,
          item.release_year,
          `"${(item.rating || '').replace(/"/g, '""')}"`,
          `"${(item.duration || '').replace(/"/g, '""')}"`,
          `"${(item.listed_in || '').replace(/"/g, '""')}"`
        ];
        csvContent += row.join(',') + '\n';
      });

      const encodedUri = encodeURI(csvContent);
      const link = document.createElement('a');
      link.setAttribute('href', encodedUri);
      link.setAttribute('download', 'netflix_analytics_catalog.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });
  }

  // ============================================================================
  // FLOATING BACK TO TOP BUTTON
  // ============================================================================
  function initBackToTop() {
    const backBtn = document.getElementById('backToTopBtn');
    if (!backBtn) return;

    window.addEventListener('scroll', () => {
      if (window.scrollY > 400) {
        backBtn.classList.add('visible');
      } else {
        backBtn.classList.remove('visible');
      }
    });

    backBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
});
