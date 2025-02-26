const express = require('express');
const axios = require('axios');
const moment = require('moment');
require('dotenv').config();

const app = express();
const port = 8080;

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Error handling middleware
app.use((err, req, res, next) => {
    console.error('Error:', err.message);
    res.status(500).json({ error: 'Internal server error' });
});

// News API configuration
const NEWS_API_KEY = process.env.NEWS_API_KEY;
const NEWS_API_URL = 'https://newsapi.org/v2/everything';

// Fetch news data
async function fetchNews(startDate, endDate) {
    try {
        console.log(`Fetching news from ${startDate} to ${endDate}`);
        const response = await axios.get(NEWS_API_URL, {
            params: {
                q: 'bitcoin',
                from: startDate,
                to: endDate,
                language: 'en',
                sortBy: 'publishedAt',
                apiKey: NEWS_API_KEY
            }
        });

        if (response.data.status !== 'ok') {
            console.error('API Error:', response.data.message);
            return [];
        }

        console.log(`Fetched ${response.data.articles.length} articles`);
        return response.data.articles;
    } catch (error) {
        console.error('Error fetching news:', error.message);
        return [];
    }
}

// Process news data
function processNewsData(articles) {
    return articles.map(article => ({
        title: article.title,
        description: article.description,
        source: article.source.name,
        publishedAt: moment(article.publishedAt).utc(),
        url: article.url
    }));
}

// API endpoints
app.get('/api/news', async (req, res) => {
    try {
        const days = parseInt(req.query.days) || 1;
        const endDate = moment().utc();
        const startDate = moment().utc().subtract(days, 'days');

        console.log(`Processing request for last ${days} days of news`);

        const articles = await fetchNews(
            startDate.format('YYYY-MM-DD'),
            endDate.format('YYYY-MM-DD')
        );

        const processedData = processNewsData(articles);

        const response = {
            total: processedData.length,
            uniqueSources: [...new Set(processedData.map(article => article.source))].length,
            recentMentions: processedData.filter(article => 
                moment().utc().diff(article.publishedAt, 'hours') <= 1
            ).length,
            articles: processedData
        };

        console.log(`Sending response with ${response.total} articles`);
        res.json(response);
    } catch (error) {
        console.error('Error processing request:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Start server
app.listen(port, '0.0.0.0', () => {
    console.log(`Server running on port ${port}`);
    console.log('Server configuration:', {
        port,
        staticPath: 'public',
        apiEndpoints: ['/api/news']
    });
});
