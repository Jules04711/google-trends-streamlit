import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time

# Initialize pytrends with increased timeout
try:
    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25))  # (connect timeout, read timeout)
except Exception as e:
    st.error(f"Failed to initialize Google Trends connection: {str(e)}")
    st.info("Please check your internet connection and try again.")
    st.stop()

# Set page config
st.set_page_config(
    page_title="Google Trends Explorer",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 Google Trends Explorer")
st.markdown("""
This app allows you to explore Google Trends data for any search term.
Enter a search term below to see its trend over time.
""")

# Sidebar for input
with st.sidebar:
    st.header("Search Settings")
    search_term = st.text_input("Enter search term:", "Python programming")
    
    # Time range selection
    time_ranges = {
        "Last 12 months": "today 12-m",
        "Last 5 years": "today 5-y",
        "Last 10 years": "today 10-y",
        "Last 24 hours": "now 1-d",
        "Last 7 days": "now 7-d",
        "Last 30 days": "today 1-m",
        "Last 90 days": "today 3-m"
    }
    selected_range = st.selectbox("Select time range:", list(time_ranges.keys()))

# Main content
if search_term:
    try:
        # Add retry mechanism
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                # Build payload
                pytrends.build_payload([search_term], timeframe=time_ranges[selected_range], geo='US')
                
                # Get interest over time
                interest_over_time_df = pytrends.interest_over_time()
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    st.warning(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                else:
                    raise e
        
        if not interest_over_time_df.empty:
            # Reset index to make date a column
            interest_over_time_df = interest_over_time_df.reset_index()
            
            # Ensure all columns are numeric except date
            for col in interest_over_time_df.columns:
                if col != 'date':
                    interest_over_time_df[col] = pd.to_numeric(interest_over_time_df[col], errors='coerce')
            
            # Create line plot
            fig = px.line(
                interest_over_time_df,
                x='date',
                y=search_term,
                title=f"Interest over time for '{search_term}'",
                labels={'date': 'Date', 'value': 'Interest'},
                template='plotly_white'
            )
            
            # Update layout
            fig.update_layout(
                height=500,
                showlegend=False,
                title_x=0.5,
                title_font_size=20
            )
            
            # Display the plot
            st.plotly_chart(fig, use_container_width=True)
            
            # Display raw data
            st.subheader("Raw Data")
            st.dataframe(interest_over_time_df)
            
        else:
            st.warning("No data available for the selected search term and time range.")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("""
        If you're experiencing connection issues:
        1. Check your internet connection
        2. Try again in a few minutes
        3. If the problem persists, try using a VPN
        """)
else:
    st.info("Please enter a search term in the sidebar to see the trends.") 