import pandas as pd
from typing import List, Dict
from datetime import datetime
import pytz

def process_news_data(articles: List[Dict]) -> pd.DataFrame:
    """
    Process raw news data into a pandas DataFrame
    """
    if not articles:
        return pd.DataFrame()

    # Create DataFrame
    df = pd.DataFrame(articles)

    # Clean and transform data
    df['published_at'] = pd.to_datetime(df['publishedAt']).dt.tz_localize('UTC')
    df['source'] = df['source'].apply(lambda x: x['name'])

    # Extract relevant columns
    df = df[[
        'title',
        'description',
        'source',
        'published_at',
        'url'
    ]]

    # Sort by publication date
    df = df.sort_values('published_at', ascending=False)

    # Remove duplicates
    df = df.drop_duplicates(subset=['title', 'source'])

    return df