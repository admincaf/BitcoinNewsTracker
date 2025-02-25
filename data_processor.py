import pandas as pd
from typing import List, Dict
from datetime import datetime
import pytz
import traceback

def process_news_data(articles: List[Dict]) -> pd.DataFrame:
    """
    Process raw news data into a pandas DataFrame
    """
    try:
        if not articles:
            print("No articles received from API")
            return pd.DataFrame()

        # Create DataFrame
        df = pd.DataFrame(articles)

        # Print raw data for debugging
        print("Raw data sample:", df.head(1).to_dict())

        # Clean and transform data
        try:
            # First convert to datetime without timezone
            df['published_at'] = pd.to_datetime(df['publishedAt'])
            # Then explicitly set UTC timezone
            if df['published_at'].dt.tz is None:
                df['published_at'] = df['published_at'].dt.tz_localize('UTC')

            df['source'] = df['source'].apply(lambda x: x['name'] if isinstance(x, dict) else str(x))
        except Exception as e:
            print(f"Error in data transformation: {str(e)}\n{traceback.format_exc()}")
            raise

        # Extract relevant columns
        try:
            df = df[[
                'title',
                'description',
                'source',
                'published_at',
                'url'
            ]]
        except KeyError as e:
            print(f"Missing required columns: {str(e)}")
            print("Available columns:", df.columns.tolist())
            raise

        # Sort by publication date
        df = df.sort_values('published_at', ascending=False)

        # Remove duplicates
        df = df.drop_duplicates(subset=['title', 'source'])

        # Print processed data for debugging
        print("Processed data sample:", df.head(1).to_dict())
        return df

    except Exception as e:
        print(f"Error in process_news_data: {str(e)}\n{traceback.format_exc()}")
        return pd.DataFrame()