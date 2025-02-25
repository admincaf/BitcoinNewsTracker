import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import traceback

def create_trend_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a line chart showing Bitcoin mentions over time
    """
    try:
        if df.empty:
            print("Empty DataFrame provided to create_trend_chart")
            return go.Figure()

        # Ensure we're working with timezone-aware data
        df_copy = df.copy()

        # Print debug info
        print("Trend chart input data sample:", df_copy.head(1).to_dict())
        print("Published_at dtype:", df_copy['published_at'].dtype)

        # Group by hour and count mentions
        mentions_by_time = df_copy.groupby(
            pd.Grouper(key='published_at', freq='h')
        ).size().reset_index()
        mentions_by_time.columns = ['timestamp', 'mentions']

        # Create the line chart
        fig = px.line(
            mentions_by_time,
            x='timestamp',
            y='mentions',
            title='Bitcoin Mentions Over Time'
        )

        fig.update_layout(
            xaxis_title="Time (UTC)",
            yaxis_title="Number of Mentions",
            hovermode='x unified',
            showlegend=False
        )

        return fig
    except Exception as e:
        print(f"Error creating trend chart: {str(e)}\n{traceback.format_exc()}")
        return go.Figure()

def create_source_breakdown(df: pd.DataFrame) -> go.Figure:
    """
    Create a bar chart showing mentions by news source
    """
    try:
        if df.empty:
            print("Empty DataFrame provided to create_source_breakdown")
            return go.Figure()

        # Print debug info
        print("Source breakdown input data sample:", df.head(1).to_dict())

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
        print(f"Error creating source breakdown: {str(e)}\n{traceback.format_exc()}")
        return go.Figure()