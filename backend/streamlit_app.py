"""Module docstring: This module contains the Streamlit app for displaying different financial data types."""

import tracemalloc
import warnings
from io import StringIO

import pandas as pd
import requests
import streamlit as st

# Initialization code such as tracemalloc.start() and setting up warnings
tracemalloc.start()
warnings.filterwarnings("ignore", message="coroutine 'expire_cache' was never awaited", category=RuntimeWarning)


def setup_page_config():
    """Sets up page configurations."""
    st.set_page_config(page_title="API-Powered Backtesting", page_icon=":chart_with_upwards_trend:", layout='wide')
    st.image("images/algoAI_large.png", width=300)  # Adjust width as needed


def display_tabs():
    """
    Creates tabs for different types of financial data.
    :return: The tabs for the different types of financial data.
    :rtype: streamlit.Tabs
    """
    return st.tabs(["Share Prices", "Crypto Prices", "Forex Prices", "Commodities Prices", "Economic Indicators",
                    "Technical Indicators"])


def share_prices(tab):
    """Functionality for the Share Prices tab."""
    with tab:
        # Configuration inputs in the sidebar
        with st.sidebar:
            config = {
                'symbol': st.text_input('Symbol', 'NVDA', key="share_symbol"),
                'function': st.selectbox('Function',
                                         ['TIME_SERIES_INTRADAY', 'TIME_SERIES_DAILY', 'TIME_SERIES_DAILY_ADJUSTED',
                                          'TIME_SERIES_WEEKLY', 'TIME_SERIES_WEEKLY_ADJUSTED', 'TIME_SERIES_MONTHLY',
                                          'TIME_SERIES_MONTHLY_ADJUSTED'], key="share_function"),
                'interval': st.selectbox('Interval', ['1min', '5min', '15min', '30min', '60min'], key="share_interval"),
                'data_type': st.selectbox('Data Type', ['json', 'csv'], key="share_data_type"),
                'output_size': st.selectbox('Output Size', ['compact', 'full'], key="share_output_size"),
                'extended': st.checkbox('Extended Hours', False, key="share_extended"),
                'api_key': st.text_input('API Key', 'demo', key="share_api_key")
            }

        # Move Fetch Data button and data display out of the sidebar
        st.markdown(f"<span style='font-size: 18.3px;'>{config['symbol'].upper()} Share Prices</span>",
                    unsafe_allow_html=True)

        if st.button('Fetch Data', key="share_fetch"):
            api_request = AlphaVantageRequest(config)
            url = api_request.build_url()
            data = APIRequest.get_data(url)  # This should be returning a string if get_data is correctly implemented

            if config['data_type'] == 'json':
                st.json(data)
            else:  # Assume CSV
                # Convert string data to DataFrame
                data_io = StringIO(data)  # This should no longer cause a TypeError
                df = pd.read_csv(data_io)
                st.table(df)


class APIRequest:
    @staticmethod
    @st.cache_data(ttl=600)  # Cache data for 10 minutes; adjust TTL as needed
    def get_data(url):
        """Fetch data from the constructed URL."""
        response = requests.get(url, timeout=10)  # Timeout after 10 seconds
        return response.text  # Make sure to return response.text, not just response

    def build_url(self):
        """
        This is an abstract method. It should be implemented by subclasses.
        :return: The constructed URL.
        :rtype: str
        """
        raise NotImplementedError("Subclass must implement abstract method")


class AlphaVantageRequest(APIRequest):
    """Class for constructing requests to the Alpha Vantage API."""

    def __init__(self, config):
        self.config = config

    def build_url(self):
        extended_str = 'true' if self.config['extended'] else 'false'
        return (f"https://www.alphavantage.co/query"
                f"?function={self.config['function']}"
                f"&symbol={self.config['symbol']}"
                f"&interval={self.config['interval']}"
                f"&datatype={self.config['data_type']}"
                f"&outputsize={self.config['output_size']}"
                f"&extended_hours={extended_str}"
                f"&apikey={self.config['api_key']}")


def main():
    """
    Main function for the Streamlit app.
    :return: None
    """
    setup_page_config()
    tabs = display_tabs()
    share_prices(tabs[0])


if __name__ == "__main__":
    main()
