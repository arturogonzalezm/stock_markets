import pytest
import pandas as pd
from backend.shares import plot_candlestick_chart, AlphaVantageRequest


# Fixture for a DataFrame with a 'timestamp' column
@pytest.fixture
def df_with_timestamp():
    return pd.DataFrame({
        'timestamp': ['2022-01-01', '2022-01-02'],
        'open': [100, 110],
        'high': [120, 130],
        'low': [90, 100],
        'close': [110, 120]
    })


# Fixture for a DataFrame without a 'timestamp' column
@pytest.fixture
def df_without_timestamp():
    return pd.DataFrame({
        'open': [100, 110],
        'high': [120, 130],
        'low': [90, 100],
        'close': [110, 120]
    })


# Fixture for AlphaVantageRequest configuration
@pytest.fixture
def alpha_vantage_config():
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


# Test plot_candlestick_chart with timestamp
def test_plot_candlestick_chart_with_timestamp(df_with_timestamp):
    # Assuming plot_candlestick_chart function returns something or use pytest.raises to check for exceptions
    plot_candlestick_chart(df_with_timestamp)


# Test plot_candlestick_chart without timestamp
def test_plot_candlestick_chart_without_timestamp(df_without_timestamp):
    # Assuming plot_candlestick_chart function returns something or use pytest.raises to check for exceptions
    plot_candlestick_chart(df_without_timestamp)


# Test AlphaVantageRequest URL building
def test_build_url(alpha_vantage_config):
    av_request = AlphaVantageRequest(alpha_vantage_config)
    url = av_request.build_url()
    assert url.startswith("https://www.alphavantage.co/query")
    assert "function=TIME_SERIES_INTRADAY" in url
    assert "symbol=AAPL" in url
    assert "interval=5min" in url
    assert "datatype=json" in url
    assert "outputsize=compact" in url
    assert "extended_hours=false" in url
    assert "apikey=your_api_key" in url
    assert "month=2023-01" in url
