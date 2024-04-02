import pytest
import requests
import pandas as pd
from unittest.mock import patch, MagicMock
from backend.shares import APIRequest, AlphaVantageRequest, plot_candlestick_chart


def test_api_request_get_data_success():
    with patch('requests.get') as mock_get:
        mock_get.return_value.content = b'success'
        url = 'http://test.com'
        assert APIRequest.get_data(url) == b'success'


def test_api_request_get_data_failure():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException
        url = 'http://test.com'
        with pytest.raises(requests.exceptions.RequestException):
            APIRequest.get_data(url)


def test_alpha_vantage_request_build_url():
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
    url = av_request.build_url()
    assert url == ("https://www.alphavantage.co/query"
                   "?function=TIME_SERIES_INTRADAY"
                   "&symbol=AAPL"
                   "&interval=5min"
                   "&datatype=json"
                   "&outputsize=compact"
                   "&extended_hours=false"
                   "&apikey=your_api_key"
                   "&month=2023-01")


def test_plot_candlestick_chart_with_empty_dataframe():
    df = pd.DataFrame()
    with patch('streamlit.warning') as mock_warning:
        plot_candlestick_chart(df)
        mock_warning.assert_called_once_with("DataFrame does not contain 'timestamp' column.")


def test_plot_candlestick_chart_with_invalid_dataframe():
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
