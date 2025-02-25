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

        # Group by hour and count mentions
        try:
            # Ensure datetime is in UTC
            df_copy = df.copy()
            if df_copy['published_at'].dt.tz is None:
                df_copy['published_at'] = df_copy['published_at'].dt.tz_localize('UTC')

            # Group by hour
            mentions_by_time = df_copy.groupby(
                pd.Grouper(key='published_at', freq='H')
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
            print(f"Error in trend chart data processing: {str(e)}")
            return go.Figure()

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

        # Get source counts
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
            print(f"Error in source breakdown data processing: {str(e)}")
            return go.Figure()

    except Exception as e:
        print(f"Error creating source breakdown: {str(e)}\n{traceback.format_exc()}")
        return go.Figure()