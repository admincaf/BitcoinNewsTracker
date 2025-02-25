import requests
import os
from datetime import datetime
from typing import List, Dict
import traceback

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_news(start_date: datetime, end_date: datetime) -> List[Dict]:
    """
    Fetch news articles containing 'bitcoin' from NewsAPI
    """
    try:
        if not NEWS_API_KEY:
            print("Error: NEWS_API_KEY environment variable is not set")
            return []

        params = {
            'q': 'bitcoin',
            'from': start_date.strftime('%Y-%m-%d'),
            'to': end_date.strftime('%Y-%m-%d'),
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': NEWS_API_KEY
        }

        print(f"Fetching news from {start_date} to {end_date}")

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            print(f"API Response status: {data.get('status')}")
            print(f"Total results: {data.get('totalResults', 0)}")

            if data.get('status') != 'ok':
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return []

            articles = data.get('articles', [])
            print(f"Retrieved {len(articles)} articles")

            if not articles:
                print("No articles found in the response")

            return articles

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return []

    except Exception as e:
        print(f"Unexpected error in fetch_news: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return []