# At the beginning of your script
"""Module docstring: This module contains the Streamlit app for displaying different financial data types."""
# This is the module-level docstring describing what this module does.

# Imports come here
import tracemalloc
import warnings
from io import StringIO

import pandas as pd
import numpy as np
import requests
import streamlit as st
import plotly.graph_objects as go

# Initialization code such as tracemalloc.start() and setting up warnings
tracemalloc.start()
warnings.filterwarnings("ignore", message="coroutine 'expire_cache' was never awaited", category=RuntimeWarning)


# Function to plot the candlestick chart
def plot_candlestick_chart(df):
    """
    Plot candlestick chart based on the provided DataFrame.
    :param df: DataFrame containing the data to plot.
    :return: None
    """
    if 'timestamp' in df.columns:
        fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                                             open=df['open'],
                                             high=df['high'],
                                             low=df['low'],
                                             close=df['close'])])

        fig.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True}, height=700)
    else:
        st.warning("DataFrame does not contain 'timestamp' column.")


# Function to set up page configurations
def setup_page_config():
    """
    Sets up page configurations.
    :return: None
    """
    st.set_page_config(page_title="Streamlit Financial Data Visualization App",
                       page_icon=":chart_with_upwards_trend:",
                       layout='wide')
    st.image("images/algoAI_large.png", width=300)  # Adjust width as needed


# Function to create tabs for different types of financial data
def display_tabs():
    """
    Creates tabs for different types of financial data.
    :return: The tabs for the different types of financial data.
    :rtype: streamlit.Tabs
    """
    return st.tabs(["Share Prices",
                    "Crypto Prices",
                    "Forex Prices",
                    "Commodities Prices",
                    "Economic Indicators",
                    "Technical Indicators"])


def simulate_trading_based_on_moving_average(df):
    """
    Simulates trading decisions based on moving average crossover strategy.
    :param df: DataFrame containing the price data.
    :return: None
    """
    # Calculate short-term (20-day) and long-term (50-day) moving averages
    df['short_ma'] = df['close'].rolling(window=20).mean()
    df['long_ma'] = df['close'].rolling(window=50).mean()

    # Identify crossovers
    df['signal'] = np.where(df['short_ma'] > df['long_ma'], 'buy', 'sell')

    # Simulate a trading decision based on the latest data
    latest_decision = df['signal'].iloc[-1]
    st.write(f"Latest trading decision based on moving average strategy: **{latest_decision.upper()}**")


# Functionality for the Share Prices tab
def share_prices(tab):
    """
    Functionality for the Share Prices tab.
    :param tab: The current tab.
    :type tab: streamlit.Tabs
    """
    with tab:
        # Configuration inputs in the sidebar
        with st.sidebar:
            config = {
                'symbol': st.text_input('Symbol', 'NVDA', key="share_symbol"),
                'function': st.selectbox('Function',
                                         ['TIME_SERIES_INTRADAY',
                                          'TIME_SERIES_DAILY',
                                          'TIME_SERIES_DAILY_ADJUSTED',
                                          'TIME_SERIES_WEEKLY',
                                          'TIME_SERIES_WEEKLY_ADJUSTED',
                                          'TIME_SERIES_MONTHLY',
                                          'TIME_SERIES_MONTHLY_ADJUSTED'], key="share_function"),
                'interval': st.selectbox('Interval', ['1min', '5min', '15min', '30min', '60min'], key="share_interval"),
                'data_type': st.selectbox('Data Type', ['json', 'csv'], key="share_data_type"),
                'output_size': st.selectbox('Output Size', ['compact', 'full'], key="share_output_size"),
                'extended': st.toggle('Extended Hours', False, key="share_extended"),
                'month': st.text_input('Month', '2009-01', key="share_month"),
                'api_key': st.text_input('API Key', 'demo', key="share_api_key", type="password")
            }

        # Fetch data based on the sidebar inputs
        api_request = AlphaVantageRequest(config)
        url = api_request.build_url()
        data = APIRequest.get_data(url)  # This should be returning bytes if get_data is correctly implemented

        # Move Fetch Data button and data display out of the sidebar
        st.markdown(
            f"<span style='font-size: 19px;'>{config['symbol'].upper()} :blue[Share Prices]</span>",
            unsafe_allow_html=True
        )

        if config['data_type'] == 'json':
            st.json(data)
        else:  # Assume CSV
            # Convert bytes data to DataFrame
            data_io = StringIO(data.decode('utf-8'))
            df = pd.read_csv(data_io)

            # Plot candlestick chart
            plot_candlestick_chart(df)

            # Display DataFrame with adjustable width
            st.dataframe(df.style.set_table_styles(
                [dict(selector='table', props=[('max-height', '400px'), ('overflow-y', 'scroll'), ('width', '100%')])]
            ), width=1300)


# Class for handling API requests
class APIRequest:
    @staticmethod
    @st.cache_data(ttl=600)  # Cache data for 10 minutes; adjust TTL as needed
    def get_data(url):
        """
        Fetch data from the constructed URL.
        :param url: The URL to fetch data from.
        :return: The data fetched from the URL.
        :rtype: bytes
        """
        response = requests.get(url, timeout=10)  # Timeout after 10 seconds
        return response.content  # Return response.content instead of response.text

    def build_url(self):
        """
        This is an abstract method. It should be implemented by subclasses.
        :return: The constructed URL.
        :rtype: str
        """
        raise NotImplementedError("Subclass must implement abstract method")


# Class for handling requests to the Alpha Vantage API
class AlphaVantageRequest:
    """Handles construction and representation of requests to the Alpha Vantage API."""

    def __init__(self, config):
        # initialization code
        self.config = config

    def build_url(self):
        """
        Constructs the URL for the API request.
        :return: The constructed URL.
        :rtype: str
        :raises NotImplementedError: If the function is not implemented by the subclass.
        """
        extended_str = 'true' if self.config['extended'] else 'false'
        return (f"https://www.alphavantage.co/query"
                f"?function={self.config['function']}"
                f"&symbol={self.config['symbol']}"
                f"&interval={self.config['interval']}"
                f"&datatype={self.config['data_type']}"
                f"&outputsize={self.config['output_size']}"
                f"&extended_hours={extended_str}"
                f"&apikey={self.config['api_key']}"
                f"&month={self.config['month']}")
