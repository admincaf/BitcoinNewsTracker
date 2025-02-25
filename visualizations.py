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

        # Ensure we have the right columns
        if 'published_at' not in df.columns:
            print("Missing 'published_at' column")
            return go.Figure()

        # Create a copy for manipulation
        df_copy = df.copy()

        # Ensure datetime is timezone-aware
        if df_copy['published_at'].dt.tz is None:
            df_copy['published_at'] = df_copy['published_at'].dt.tz_localize('UTC')

        # Create hourly bins for the entire date range
        min_date = df_copy['published_at'].min()
        max_date = df_copy['published_at'].max()
        date_range = pd.date_range(start=min_date, end=max_date, freq='h', tz='UTC')

        # Count mentions by hour
        mentions = df_copy.groupby(
            pd.Grouper(key='published_at', freq='h')
        ).size().reindex(date_range, fill_value=0)

        # Create dataframe for plotting
        plot_df = pd.DataFrame({
            'timestamp': mentions.index,
            'mentions': mentions.values
        })

        # Create the line chart
        fig = px.line(
            plot_df,
            x='timestamp',
            y='mentions',
            title='Bitcoin Mentions Over Time'
        )

        # Update layout
        fig.update_layout(
            xaxis_title="Time (UTC)",
            yaxis_title="Number of Mentions",
            hovermode='x unified',
            showlegend=False,
            xaxis=dict(
                tickformat="%Y-%m-%d %H:%M",
                tickangle=45
            )
        )

        return fig

    except Exception as e:
        print(f"Error creating trend chart: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return go.Figure()

def create_source_breakdown(df: pd.DataFrame) -> go.Figure:
    """
    Create a bar chart showing mentions by news source
    """
    try:
        if df.empty:
            print("Empty DataFrame provided to create_source_breakdown")
            return go.Figure()

        if 'source' not in df.columns:
            print("Missing 'source' column")
            return go.Figure()

        # Get source counts
        source_counts = df['source'].value_counts().head(10)

        # Create the bar chart
        fig = px.bar(
            x=source_counts.index,
            y=source_counts.values,
            title='Top News Sources Mentioning Bitcoin',
            labels={'x': 'News Source', 'y': 'Number of Mentions'}
        )

        # Update layout
        fig.update_layout(
            xaxis_tickangle=45,
            showlegend=False,
            xaxis_title="News Source",
            yaxis_title="Number of Mentions",
            height=500  # Ensure enough height for labels
        )

        # Update bar appearance
        fig.update_traces(
            marker_color='rgb(55, 83, 109)',
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5
        )

        return fig

    except Exception as e:
        print(f"Error creating source breakdown: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return go.Figure()