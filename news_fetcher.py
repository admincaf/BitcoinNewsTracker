import requests
from datetime import datetime
from typing import List, Dict

NEWS_API_KEY = "YOUR_NEWS_API_KEY"  # Replace with actual API key
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_news(start_date: datetime, end_date: datetime) -> List[Dict]:
    """
    Fetch news articles containing 'bitcoin' from NewsAPI
    """
    params = {
        'q': 'bitcoin',
        'from': start_date.strftime('%Y-%m-%d'),
        'to': end_date.strftime('%Y-%m-%d'),
        'language': 'en',
        'sortBy': 'publishedAt',
        'apiKey': NEWS_API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] != 'ok':
            raise Exception(f"API Error: {data.get('message', 'Unknown error')}")
            
        return data['articles']
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch news data: {str(e)}")
