import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from news_fetcher import fetch_news
from data_processor import process_news_data
from visualizations import create_trend_chart, create_daily_trend_chart, create_source_breakdown
import pytz
import traceback

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
    try:
        # Calculate date range with explicit UTC timezone
        current_time = datetime.now(pytz.UTC)
        end_date = current_time
        start_date = end_date - timedelta(days=days)

        print(f"Fetching data from {start_date} to {end_date}")

        # Fetch news data
        news_data = fetch_news(start_date, end_date)
        if not news_data:
            st.error("No news data available. Please try again later.")
            return pd.DataFrame()

        # Process the data
        df = process_news_data(news_data)
        if df.empty:
            st.error("Could not process news data. Please try again later.")
            return df

        print(f"Successfully processed {len(df)} articles")
        print(f"DataFrame dtypes: {df.dtypes}")
        return df

    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        print(f"Detailed error: {traceback.format_exc()}")
        return pd.DataFrame()

try:
    # Loading state
    with st.spinner('Fetching Bitcoin news data...'):
        df = get_processed_data(days)

    if not df.empty:
        # Verify timezone awareness
        if df['published_at'].dt.tz is None:
            df['published_at'] = df['published_at'].dt.tz_localize('UTC')

        # Display metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Bitcoin Mentions", len(df))

        with col2:
            st.metric("Unique Sources", df['source'].nunique())

        with col3:
            try:
                # Get current time in UTC
                current_time = pd.Timestamp.now(tz='UTC')
                one_hour_ago = current_time - pd.Timedelta(hours=1)

                # Filter recent mentions using pandas Timestamp
                recent_mentions = len(df[df['published_at'] >= one_hour_ago])
                st.metric("Mentions in Last Hour", recent_mentions)
            except Exception as e:
                print(f"Error calculating recent mentions: {str(e)}")
                st.metric("Mentions in Last Hour", "N/A")

        # Trend charts
        st.subheader("📈 Bitcoin Mention Trends")

        # Hourly trend
        trend_chart = create_trend_chart(df)
        st.plotly_chart(trend_chart, use_container_width=True)

        # Daily trend
        daily_chart = create_daily_trend_chart(df)
        st.plotly_chart(daily_chart, use_container_width=True)

        # Source breakdown
        st.subheader("📰 Mentions by News Source")
        source_chart = create_source_breakdown(df)
        st.plotly_chart(source_chart, use_container_width=True)

        # Recent mentions table
        st.subheader("📑 Recent Mentions")
        recent_df = df.head(10)[['title', 'source', 'published_at', 'url']]
        st.dataframe(
            recent_df.style.format({'published_at': lambda x: x.strftime('%Y-%m-%d %H:%M UTC')}),
            column_config={
                "url": st.column_config.LinkColumn("Article Link")
            },
            hide_index=True
        )
    else:
        st.warning("No data available. Please check your internet connection and try again.")

except Exception as e:
    st.error("An error occurred while loading the dashboard")
    print(f"Dashboard error: {str(e)}")
    print(f"Traceback: {traceback.format_exc()}")

# Footer
st.markdown("---")
st.markdown("Data updates hourly. Source: NewsAPI")