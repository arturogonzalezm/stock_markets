"""
This module contains tests for the shares functionality,
including plotting and API request building.
"""

import pytest
import pandas as pd
from requests import RequestException

# If you have import errors, ensure your PYTHONPATH is correctly set up
# or adjust your project structure.
from requests.exceptions import RequestException

from backend.shares import plot_candlestick_chart, AlphaVantageRequest


@pytest.fixture
def df_with_timestamp():
    """Fixture for DataFrame with a timestamp column."""
    return pd.DataFrame({
        'timestamp': ['2022-01-01', '2022-01-02'],
        'open': [100, 110],
        'high': [120, 130],
        'low': [90, 100],
        'close': [110, 120]
    })


@pytest.fixture
def df_without_timestamp():
    """Fixture for DataFrame without a timestamp column."""
    return pd.DataFrame({
        'open': [100, 110],
        'high': [120, 130],
        'low': [90, 100],
        'close': [110, 120]
    })


@pytest.fixture
def alpha_vantage_config():
    """Fixture for AlphaVantageRequest configuration."""
    return {
        'symbol': 'AAPL',
        'function': 'TIME_SERIES_INTRADAY',
        'interval': '5min',
        'data_type': 'json',
        'output_size': 'compact',
        'extended': False,
        'month': '2023-01',
        'api_key': 'your_api_key'
    }


def test_plot_candlestick_chart_with_timestamp(df_with_timestamp):
    """
    Test that plot_candlestick_chart function works with timestamp column.
    """
    plot_candlestick_chart(df_with_timestamp)


def test_plot_candlestick_chart_without_timestamp(df_without_timestamp):
    """
    Test that plot_candlestick_chart function handles absence of timestamp column.
    """
    plot_candlestick_chart(df_without_timestamp)


def test_alpha_vantage_request_fetch_data(alpha_vantage_config, mocker):
    """Test fetching data from AlphaVantage API handles expected scenarios."""
    mocker.patch('backend.shares.requests.get', side_effect=RequestException)

    av_request = AlphaVantageRequest(alpha_vantage_config)

    # Assuming you handle RequestException within fetch_data and return None or similar
    result = av_request.fetch_data()
    assert result is None  # or assert for a custom exception as per your implementation


def test_alpha_vantage_request_network_error(alpha_vantage_config, mocker):
    """Test AlphaVantageRequest handles network errors gracefully when fetching data."""
    # Assuming 'fetch_data' is the method that makes the network request
    # Use mocker to simulate a network error on requests.get
    mocker.patch('backend.shares.requests.get', side_effect=RequestException)

    # Initialize your AlphaVantageRequest with the test configuration
    av_request = AlphaVantageRequest(alpha_vantage_config)

    # Assume your method should handle network errors in a specific way, such as returning None or raising a custom exception
    # Here, we're assuming a custom exception named 'DataFetchError' should be raised
    with pytest.raises(RequestException):
        av_request.fetch_data()


def test_build_url(alpha_vantage_config):
    """
    Test that AlphaVantageRequest.build_url correctly constructs the request URL.
    """
    av_request = AlphaVantageRequest(alpha_vantage_config)
    url = av_request.build_url()
    expected_parts = [
        "https://www.alphavantage.co/query",
        "function=TIME_SERIES_INTRADAY",
        "symbol=AAPL",
        "interval=5min",
        "datatype=json",
        "outputsize=compact",
        "extended_hours=false",
        "apikey=your_api_key",
        "month=2023-01"
    ]
    for part in expected_parts:
        assert part in url
