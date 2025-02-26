# BitcoinNewsTracker

A real-time Bitcoin news tracking application that aggregates and visualizes mentions of Bitcoin across major news sources.

## Features

- Real-time tracking of Bitcoin mentions in news articles
- Visual representation of mention frequency (hourly and daily)
- Statistics on total mentions, unique sources, and recent activity
- Configurable time period selection
- Clean and responsive user interface

## Prerequisites

- Node.js (v14 or higher)
- NPM (Node Package Manager)
- News API Key (from [newsapi.org](https://newsapi.org))

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/admincaf/BitcoinNewsTracker.git
   cd BitcoinNewsTracker
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the root directory and add your News API key:
   ```
   NEWS_API_KEY=your_api_key_here
   ```

## Usage

1. Start the server:
   ```bash
   node server.js
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

3. Use the time period selector to view Bitcoin news mentions for different durations.

## API Endpoints

### GET /api/news
Fetches Bitcoin news articles for a specified time period.

Query Parameters:
- `days` (optional): Number of days to fetch news for (default: 1)

Response Format:
```json
{
  "total": number,
  "uniqueSources": number,
  "recentMentions": number,
  "articles": [
    {
      "title": string,
      "description": string,
      "source": string,
      "publishedAt": string,
      "url": string
    }
  ]
}
```

## Tech Stack

- Frontend: HTML, CSS, JavaScript, Chart.js
- Backend: Node.js, Express
- APIs: News API
- Data Visualization: Chart.js

## License

ISC
