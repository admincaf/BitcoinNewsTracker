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
        print(f"Raw DataFrame columns: {df.columns.tolist()}")
        print(f"Raw data first row: {df.iloc[0].to_dict() if not df.empty else 'Empty DataFrame'}")

        # Clean and transform data
        if 'publishedAt' not in df.columns:
            print("Error: 'publishedAt' column not found")
            return pd.DataFrame()

        # Convert timestamps
        try:
            df['published_at'] = pd.to_datetime(df['publishedAt'])
            if df['published_at'].dt.tz is None:
                df['published_at'] = df['published_at'].dt.tz_localize('UTC')
        except Exception as e:
            print(f"Error converting timestamps: {e}")
            return pd.DataFrame()

        # Extract source names
        try:
            df['source'] = df['source'].apply(
                lambda x: x.get('name', str(x)) if isinstance(x, dict) else str(x)
            )
        except Exception as e:
            print(f"Error extracting source names: {e}")
            return pd.DataFrame()

        # Select and rename columns
        try:
            required_cols = ['title', 'description', 'source', 'published_at', 'url']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                print(f"Missing columns: {missing_cols}")
                return pd.DataFrame()

            df = df[required_cols]
        except Exception as e:
            print(f"Error selecting columns: {e}")
            return pd.DataFrame()

        # Sort and deduplicate
        df = df.sort_values('published_at', ascending=False)
        df = df.drop_duplicates(subset=['title', 'source'])

        print(f"Processed DataFrame shape: {df.shape}")
        print(f"Processed data first row: {df.iloc[0].to_dict() if not df.empty else 'Empty DataFrame'}")

        return df

    except Exception as e:
        print(f"Error in process_news_data: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return pd.DataFrame()