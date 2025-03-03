# google-trends-streamlit

A Streamlit web application that allows you to explore Google Trends data for any search term. The app provides interactive visualizations and raw data for the selected search term over different time periods.

## Demo


https://github.com/user-attachments/assets/b478abf8-8d99-4ef4-ba01-9d4d1d18642f


## Features

- Search for any term and see its Google Trends data
- Select different time ranges (24 hours to 10 years)
- Interactive line chart visualization
- Raw data display
- Clean and intuitive user interface

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

To run the app, execute:
```bash
streamlit run app.py
```

The app will open in your default web browser. If it doesn't, you can manually open the URL shown in the terminal (typically http://localhost:8501).

## Usage

1. Enter a search term in the sidebar
2. Select a time range from the dropdown menu
3. View the interactive chart and raw data

## Note

This app uses the pytrends library to fetch data from Google Trends. The data is normalized on a scale of 0-100, where 100 represents the peak popularity for the term. 
