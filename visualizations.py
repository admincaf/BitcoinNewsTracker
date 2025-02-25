import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def create_trend_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a line chart showing Bitcoin mentions over time
    """
    # Resample data by hour
    mentions_by_time = df.set_index('published_at').resample('H').size().reset_index()
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

def create_source_breakdown(df: pd.DataFrame) -> go.Figure:
    """
    Create a bar chart showing mentions by news source
    """
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
