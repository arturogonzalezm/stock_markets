# Import necessary modules and classes
import pytest
import pandas as pd
from backend.shares import plot_candlestick_chart, AlphaVantageRequest


# Define test cases for plot_candlestick_chart function
def test_plot_candlestick_chart_with_timestamp():
    # Create a DataFrame with required columns
    df = pd.DataFrame({
        'timestamp': ['2022-01-01', '2022-01-02'],
        'open': [100, 110],
        'high': [120, 130],
        'low': [90, 100],
        'close': [110, 120]
    })

    # Call the function with the DataFrame
    plot_candlestick_chart(df)

    # Assert that the function does not raise any errors


def test_plot_candlestick_chart_without_timestamp():
    # Create a DataFrame without the required 'timestamp' column
    df = pd.DataFrame({
        'open': [100, 110],
        'high': [120, 130],
        'low': [90, 100],
        'close': [110, 120]
    })

    # Call the function with the DataFrame
    plot_candlestick_chart(df)

    # Assert that the function does not raise any errors


# Define test cases for AlphaVantageRequest class
def test_build_url():
    # Create a configuration dictionary
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

    # Create an instance of AlphaVantageRequest
    av_request = AlphaVantageRequest(config)

    # Call the build_url method
    url = av_request.build_url()

    # Assert that the URL is constructed correctly
    assert url.startswith("https://www.alphavantage.co/query")
    assert "function=TIME_SERIES_INTRADAY" in url
    assert "symbol=AAPL" in url
    assert "interval=5min" in url
    assert "datatype=json" in url
    assert "outputsize=compact" in url
    assert "extended_hours=false" in url
    assert "apikey=your_api_key" in url
    assert "month=2023-01" in url


# Run the tests if the script is executed directly
if __name__ == "__main__":
    pytest.main()
