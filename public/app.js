// Chart configurations
let hourlyChart, dailyChart, sourcesChart;

// Initialize charts
function initializeCharts() {
    const hourlyCtx = document.getElementById('hourlyChart').getContext('2d');
    const dailyCtx = document.getElementById('dailyChart').getContext('2d');
    const sourcesCtx = document.getElementById('sourcesChart').getContext('2d');

    hourlyChart = new Chart(hourlyCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Mentions',
                data: [],
                borderColor: '#3498db',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    dailyChart = new Chart(dailyCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Mentions',
                data: [],
                backgroundColor: '#3498db'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    sourcesChart = new Chart(sourcesCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Articles',
                data: [],
                backgroundColor: '#3498db'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y'
        }
    });
}

// Process data for charts
function processChartData(articles) {
    // Hourly data
    const hourlyData = {};
    articles.forEach(article => {
        const hour = moment(article.publishedAt).startOf('hour').format();
        hourlyData[hour] = (hourlyData[hour] || 0) + 1;
    });

    // Daily data
    const dailyData = {};
    articles.forEach(article => {
        const day = moment(article.publishedAt).startOf('day').format('YYYY-MM-DD');
        dailyData[day] = (dailyData[day] || 0) + 1;
    });

    // Source data
    const sourceData = {};
    articles.forEach(article => {
        sourceData[article.source] = (sourceData[article.source] || 0) + 1;
    });

    return { hourlyData, dailyData, sourceData };
}

// Update charts
function updateCharts(data) {
    const { hourlyData, dailyData, sourceData } = processChartData(data.articles);

    // Update hourly chart
    const sortedHourlyData = Object.entries(hourlyData)
        .sort(([timeA], [timeB]) => moment(timeA).diff(moment(timeB)))
        .reduce((acc, [time, count]) => {
            acc.labels.push(moment(time).format('MM/DD HH:mm'));
            acc.counts.push(count);
            return acc;
        }, { labels: [], counts: [] });

    hourlyChart.data.labels = sortedHourlyData.labels;
    hourlyChart.data.datasets[0].data = sortedHourlyData.counts;
    hourlyChart.options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                type: 'category',
                display: true,
                title: {
                    display: true,
                    text: 'Time (UTC)'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Number of Mentions'
                }
            }
        },
        plugins: {
            tooltip: {
                mode: 'index',
                intersect: false
            }
        }
    };
    hourlyChart.update();

    // Update daily chart
    dailyChart.data.labels = Object.keys(dailyData);
    dailyChart.data.datasets[0].data = Object.values(dailyData);
    dailyChart.update();

    // Update sources chart
    const topSources = Object.entries(sourceData)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
    sourcesChart.data.labels = topSources.map(([source]) => source);
    sourcesChart.data.datasets[0].data = topSources.map(([, count]) => count);
    sourcesChart.update();
}

// Update metrics
function updateMetrics(data) {
    document.getElementById('totalMentions').textContent = data.total;
    document.getElementById('uniqueSources').textContent = data.uniqueSources;
    document.getElementById('recentMentions').textContent = data.recentMentions;
}

// Update recent articles
function updateRecentArticles(articles) {
    const container = document.getElementById('recentArticles');
    container.innerHTML = articles.slice(0, 10).map(article => `
        <div class="article-card">
            <h3>${article.title}</h3>
            <p class="source">${article.source} - ${moment(article.publishedAt).format('YYYY-MM-DD HH:mm')} UTC</p>
            <a href="${article.url}" target="_blank">Read More</a>
        </div>
    `).join('');
}

// Fetch and update data
async function fetchData() {
    try {
        const days = document.getElementById('timeRange').value;
        const response = await fetch(`/api/news?days=${days}`);
        const data = await response.json();

        updateMetrics(data);
        updateCharts(data);
        updateRecentArticles(data.articles);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    fetchData();

    // Set up event listeners
    document.getElementById('timeRange').addEventListener('change', fetchData);

    // Refresh data periodically
    setInterval(fetchData, 3600000); // Refresh every hour
});
