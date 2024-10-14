import pandas as pd
import requests
import streamlit as st

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"


def get_cryptocurrency_data(crypto_id, days):
    url = f"{COINGECKO_API_URL}/coins/{crypto_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


def format_chart_data(data):
    prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    prices['timestamp'] = pd.to_datetime(prices['timestamp'], unit='ms')
    return prices


st.set_page_config(page_title="Cryptocurrency Market Analysis", layout="wide")

st.title("Cryptocurrency Market Analysis")
st.subheader("Analyze cryptocurrency trends using CoinGecko API data")

st.sidebar.header("Settings")

crypto_list = ["bitcoin", "ethereum", "litecoin"]
crypto_id = st.sidebar.selectbox("Select Cryptocurrency", crypto_list)

days = st.sidebar.slider("Select Number of Days", 1, 365, 30)

if st.sidebar.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        data = get_cryptocurrency_data(crypto_id, days)
        prices = format_chart_data(data)
        st.success("Data fetched successfully!")

        st.header("Price Over Time")
        st.line_chart(prices.set_index('timestamp')['price'])

        st.header("Daily Closing Prices")
        daily_closing_prices = prices.set_index('timestamp').resample('D').last()
        st.bar_chart(daily_closing_prices['price'])

        st.header("Price Distribution")
        st.area_chart(prices.set_index('timestamp')['price'])

        st.header("Global Cryptocurrency Activity")
        st.map()

        st.header("Raw Data")
        st.dataframe(prices)

        st.success("Cryptocurrency data displayed successfully!")
else:
    st.info("Click the 'Fetch Data' button to display cryptocurrency data")

if st.checkbox("Show Additional Information"):
    st.markdown("""
        **Data Source**: CoinGecko API
        **Features**:
        - Line chart for price trends.
        - Bar chart for daily closing prices.
        - Area chart for price distribution.
        - Interactive map for global activity.
        - Raw data table.
    """)

try:

    pass
except Exception as e:
    st.error(f"An error occurred: {e}")
