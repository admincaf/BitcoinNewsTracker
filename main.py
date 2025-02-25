import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
import traceback
from news_fetcher import fetch_news
from data_processor import process_news_data
from visualizations import create_trend_chart, create_daily_trend_chart, create_source_breakdown

# Initialize logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    # Configure Streamlit page
    st.set_page_config(
        page_title="Bitcoin News Tracker",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False

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
            logger.debug("Starting data fetch process")
            # Calculate date range
            end_date = pd.Timestamp.now(tz='UTC')
            start_date = end_date - pd.Timedelta(days=days)

            logger.info(f"Fetching data for range: {start_date} to {end_date}")

            # Fetch news data
            news_data = fetch_news(start_date.to_pydatetime(), end_date.to_pydatetime())
            if not news_data:
                logger.warning("No news data returned from API")
                return None

            # Process the data
            df = process_news_data(news_data)
            if df.empty:
                logger.warning("Data processing resulted in empty DataFrame")
                return None

            logger.info(f"Successfully processed {len(df)} articles")
            return df

        except Exception as e:
            logger.error(f"Error in get_processed_data: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None

    # Main content
    try:
        with st.spinner('Loading Bitcoin news data...'):
            df = get_processed_data(days)

        if df is not None and not df.empty:
            # Metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Bitcoin Mentions", len(df))

            with col2:
                st.metric("Unique Sources", df['source'].nunique())

            with col3:
                current_time = pd.Timestamp.now(tz='UTC')
                one_hour_ago = current_time - pd.Timedelta(hours=1)
                recent_mentions = len(df[df['published_at'] >= one_hour_ago])
                st.metric("Mentions in Last Hour", recent_mentions)

            # Visualizations
            st.subheader("📈 Bitcoin Mention Trends")

            # Hourly trend
            hourly_chart = create_trend_chart(df)
            st.plotly_chart(hourly_chart, use_container_width=True)

            # Daily trend
            daily_chart = create_daily_trend_chart(df)
            st.plotly_chart(daily_chart, use_container_width=True)

            # Source breakdown
            st.subheader("📰 Top News Sources")
            source_chart = create_source_breakdown(df)
            st.plotly_chart(source_chart, use_container_width=True)

            # Recent articles
            st.subheader("📑 Recent Mentions")
            recent_df = df.head(10)[['title', 'source', 'published_at', 'url']]
            st.dataframe(
                recent_df.style.format({
                    'published_at': lambda x: x.strftime('%Y-%m-%d %H:%M UTC')
                }),
                column_config={
                    "url": st.column_config.LinkColumn("Article Link")
                },
                hide_index=True
            )
        else:
            st.error("Unable to load data. Please try again later.")

    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        st.error("An error occurred while loading the dashboard.")

    # Footer
    st.markdown("---")
    st.markdown("Data updates hourly. Source: NewsAPI")

except Exception as e:
    logger.critical(f"Critical error during app initialization: {str(e)}")
    logger.critical(f"Traceback: {traceback.format_exc()}")
    st.error("Failed to initialize the application. Please try again later.")