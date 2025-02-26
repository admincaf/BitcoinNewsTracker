# Bitcoin News Tracker

A real-time dashboard that tracks and visualizes Bitcoin mentions across major news sources.

## Features
- Real-time news tracking
- Interactive data visualization
- Multiple time range options (24 hours, 7 days, 30 days)
- Source breakdown analysis

## Setup

1. Install dependencies:
```bash
npm install express axios chart.js moment dotenv
```

2. Create a `.env` file in the root directory and add your NewsAPI key:
```
NEWS_API_KEY=your_api_key_here
```

3. Start the server:
```bash
node server.js
```

The application will be available at `http://localhost:5000`

## Project Structure

```
├── server.js           # Node.js backend server
├── package.json        # Project dependencies
├── .env               # Environment variables
└── public/            # Frontend assets
    ├── index.html     # Main HTML page
    ├── styles.css     # CSS styles
    └── app.js         # Frontend JavaScript
```

## API Endpoints

- GET `/api/news?days=1`: Fetch Bitcoin news for the specified number of days

## Dependencies

- Express.js: Web server framework
- Axios: HTTP client
- Chart.js: Data visualization
- Moment.js: Date handling
- dotenv: Environment variable management
