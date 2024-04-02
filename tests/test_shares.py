"""
This module contains tests for the shares functionality, specifically focusing on API data retrieval,
URL construction for Alpha Vantage API requests, and plotting functionality for financial data.
"""

# Importing in-built modules
from unittest.mock import patch

# Importing third-party modules
import pytest
import requests
import pandas as pd
import streamlit


# Placeholder class for generic API requests
class APIRequest:
    """Represents a generic API request."""
    @staticmethod
    def get_data(url):
        """
        Fetches data from a given URL.
        :param url: The URL to fetch data from.
        :return: The data fetched from the URL.
        :rtype: bytes
        """
        response = requests.get(url, timeout=5)
        return response.content


# Class dedicated to constructing and managing requests to the Alpha Vantage API
class AlphaVantageRequest:
    def __init__(self, config):
        """
        Constructor for the AlphaVantageRequest class
        :param config:
        """
        self.config = config

    def build_url(self):
        """
        Convert boolean values in config to lowercase strings and construct the URL
        :return:
        """
        modified_config = {k: str(v).lower() if isinstance(v, bool) else v for k, v in self.config.items()}
        return ("https://www.alphavantage.co/query"
                "?function={function}"
                "&symbol={symbol}"
                "&interval={interval}"
                "&datatype={data_type}"
                "&outputsize={output_size}"
                "&extended_hours={extended}"
                "&apikey={api_key}"
                "&month={month}").format(**modified_config)


# Function to plot a candlestick chart given a DataFrame
def plot_candlestick_chart(df):
    """
    Plots a candlestick chart based on the provided DataFrame
    :param df:
    :return:
    """
    if df.empty or not set(['timestamp', 'open', 'high', 'low', 'close']).issubset(df.columns):
        streamlit.warning("DataFrame does not contain required columns.")
        return
    # Check for invalid (non-numeric) data in financial columns
    if df[['open', 'high', 'low', 'close']].applymap(lambda x: isinstance(x, (int, float))).all().all() == False:
        streamlit.warning("Invalid data in 'open', 'high', 'low', or 'close' column.")
        return
    # Plotting logic would go here (omitted for brevity)


def test_api_request_get_data_success():
    """
    Test case to ensure successful data retrieval from an API
    :return:
    """
    with patch('requests.get') as mock_get:
        mock_get.return_value.content = b'success'
        url = 'http://test.com'
        assert APIRequest.get_data(url) == b'success'


def test_api_request_get_data_failure():
    """
    Test case to handle request failures gracefully
    :return:
    """
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException
        url = 'http://test.com'
        with pytest.raises(requests.exceptions.RequestException):
            APIRequest.get_data(url)


# Test case for verifying URL construction for Alpha Vantage API requests
def test_alpha_vantage_request_build_url():
    """
    Test case to verify URL construction for Alpha Vantage API requests
    :return:
    """
    config = {
        'symbol': 'AAPL',
        'function': 'TIME_SERIES_INTRADAY',
        'interval': '5min',
        'data_type': 'json',
        'output_size': 'compact',
        'extended': False,
        'month': '2023-01',
        'api_key': 'your_api_key'
    }
    av_request = AlphaVantageRequest(config)
    expected_url = ("https://www.alphavantage.co/query"
                    "?function=TIME_SERIES_INTRADAY"
                    "&symbol=AAPL"
                    "&interval=5min"
                    "&datatype=json"
                    "&outputsize=compact"
                    "&extended_hours=false"
                    "&apikey=your_api_key"
                    "&month=2023-01")
    assert av_request.build_url() == expected_url


# Test case to ensure the plotting function handles an empty DataFrame correctly
def test_plot_candlestick_chart_with_empty_dataframe():
    """
    Test case to ensure the plotting function handles an empty DataFrame correctly
    :return:
    """
    df = pd.DataFrame()
    with patch('streamlit.warning') as mock_warning:
        plot_candlestick_chart(df)
        mock_warning.assert_called_once_with("DataFrame does not contain required columns.")


# Test case to ensure the plotting function identifies and handles invalid DataFrame data
def test_plot_candlestick_chart_with_invalid_dataframe():
    """
    Test case to ensure the plotting function identifies and handles invalid DataFrame data
    :return:
    """
    df = pd.DataFrame({
        'timestamp': ['2022-01-01', '2022-01-02'],
        'open': [100, 110],
        'high': [120, 130],
        'low': [90, 100],
        'close': ['invalid', 'invalid']
    })
    with patch('streamlit.warning') as mock_warning:
        plot_candlestick_chart(df)
        mock_warning.assert_called_once_with("Invalid data in 'open', 'high', 'low', or 'close' column.")
