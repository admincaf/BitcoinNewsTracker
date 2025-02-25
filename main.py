import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from news_fetcher import fetch_news
from data_processor import process_news_data
from visualizations import create_trend_chart, create_source_breakdown
import pytz

# Page config
st.set_page_config(
    page_title="Bitcoin News Tracker",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("🔍 Bitcoin News Tracker")
st.markdown("""
    Track mentions of Bitcoin across major news sources. This dashboard updates periodically 
    and shows both real-time and historical data.
""")

# Sidebar controls
st.sidebar.header("📊 Dashboard Controls")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["24 Hours", "7 Days", "30 Days"],
    index=0
)

# Convert time range to days
range_map = {"24 Hours": 1, "7 Days": 7, "30 Days": 30}
days = range_map[time_range]

# Fetch and process data
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_processed_data(days):
    end_date = datetime.now(pytz.UTC)
    start_date = end_date - timedelta(days=days)
    news_data = fetch_news(start_date, end_date)
    return process_news_data(news_data)

try:
    df = get_processed_data(days)

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Bitcoin Mentions", len(df))
    with col2:
        st.metric("Unique Sources", df['source'].nunique())
    with col3:
        recent_cutoff = datetime.now(pytz.UTC) - timedelta(hours=1)
        recent_mentions = len(df[df['published_at'] >= recent_cutoff])
        st.metric("Mentions in Last Hour", recent_mentions)

    # Trend chart
    st.subheader("📈 Bitcoin Mention Trends")
    trend_chart = create_trend_chart(df)
    st.plotly_chart(trend_chart, use_container_width=True)

    # Source breakdown
    st.subheader("📰 Mentions by News Source")
    source_chart = create_source_breakdown(df)
    st.plotly_chart(source_chart, use_container_width=True)

    # Recent mentions table
    st.subheader("📑 Recent Mentions")
    recent_df = df.head(10)[['title', 'source', 'published_at', 'url']]
    st.dataframe(
        recent_df.style.format({'published_at': lambda x: x.strftime('%Y-%m-%d %H:%M')}),
        column_config={
            "url": st.column_config.LinkColumn("Article Link")
        },
        hide_index=True
    )

except Exception as e:
    st.error(f"Error fetching or processing data: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Data updates hourly. Source: NewsAPI")