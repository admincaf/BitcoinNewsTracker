import pandas as pd
from typing import List, Dict
from datetime import datetime
import pytz
import traceback

def process_news_data(articles: List[Dict]) -> pd.DataFrame:
    """
    Process raw news data into a pandas DataFrame with proper timezone handling
    """
    try:
        if not articles:
            print("No articles received from API")
            return pd.DataFrame()

        # Create DataFrame
        df = pd.DataFrame(articles)
        print(f"Raw DataFrame columns: {df.columns.tolist()}")

        # Verify required columns
        required_columns = {'publishedAt', 'source', 'title', 'description', 'url'}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            print(f"Missing required columns: {missing_columns}")
            return pd.DataFrame()

        # Handle timestamps
        try:
            # Convert to datetime and ensure UTC timezone
            df['published_at'] = pd.to_datetime(df['publishedAt'])
            # Add UTC timezone if not present
            if df['published_at'].dt.tz is None:
                df['published_at'] = df['published_at'].dt.tz_localize('UTC')
            else:
                # Convert to UTC if in a different timezone
                df['published_at'] = df['published_at'].dt.tz_convert('UTC')
        except Exception as e:
            print(f"Error processing timestamps: {str(e)}")
            return pd.DataFrame()

        # Process source field
        try:
            df['source'] = df['source'].apply(
                lambda x: x.get('name', str(x)) if isinstance(x, dict) else str(x)
            )
        except Exception as e:
            print(f"Error processing source field: {str(e)}")
            return pd.DataFrame()

        # Select and rename columns
        df = df[[
            'title',
            'description',
            'source',
            'published_at',
            'url'
        ]]

        # Sort by publication date and remove duplicates
        df = df.sort_values('published_at', ascending=False)
        df = df.drop_duplicates(subset=['title', 'source'])

        print(f"Successfully processed {len(df)} articles")
        return df

    except Exception as e:
        print(f"Error in process_news_data: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return pd.DataFrame()