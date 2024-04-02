"""
This module contains tests for the shares functionality,
including plotting and API request building.
"""

import pytest
import pandas as pd
# If you have import errors, ensure your PYTHONPATH is correctly set up
# or adjust your project structure.
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
