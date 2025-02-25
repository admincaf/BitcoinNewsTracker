import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def create_trend_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a line chart showing Bitcoin mentions over time
    """
    try:
        # Convert to timezone-naive for resampling
        df_copy = df.copy()
        df_copy.index = df_copy['published_at'].dt.tz_localize(None)

        # Resample data by hour
        mentions_by_time = df_copy.resample('H', on='published_at').size().reset_index()
        mentions_by_time.columns = ['timestamp', 'mentions']

        fig = px.line(
            mentions_by_time,
            x='timestamp',
            y='mentions',
            title='Bitcoin Mentions Over Time'
        )

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Number of Mentions",
            hovermode='x unified',
            showlegend=False
        )

        return fig
    except Exception as e:
        print(f"Error creating trend chart: {str(e)}")
        # Return an empty figure if there's an error
        return go.Figure()

def create_source_breakdown(df: pd.DataFrame) -> go.Figure:
    """
    Create a bar chart showing mentions by news source
    """
    try:
        source_counts = df['source'].value_counts().head(10)

        fig = px.bar(
            x=source_counts.index,
            y=source_counts.values,
            title='Top News Sources Mentioning Bitcoin'
        )

        fig.update_layout(
            xaxis_title="News Source",
            yaxis_title="Number of Mentions",
            xaxis_tickangle=45,
            showlegend=False
        )

        return fig
    except Exception as e:
        print(f"Error creating source breakdown: {str(e)}")
        # Return an empty figure if there's an error
        return go.Figure()