"""Module docstring: This module contains the Streamlit app for displaying different financial data types."""

import io
import tracemalloc
import warnings
from io import StringIO

import pandas as pd
import requests
import streamlit as st

# Initialization code such as tracemalloc.start() and setting up warnings
tracemalloc.start()
warnings.filterwarnings("ignore", message="coroutine 'expire_cache' was never awaited", category=RuntimeWarning)

# Set the page config to customize the layout and set the title of the app
st.set_page_config(page_title="API-Powered Backtesting", page_icon=":chart_with_upwards_trend:", layout='wide')

# Embedding the logo
st.image("images/algoAI_large.png", width=300)  # Adjust width as needed

# App title
# st.title("AI-Powered Backtesting")

# Create tabs for different types of financial data
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Share Prices", "Crypto Prices", "Forex Prices", "Commodities Prices", "Economic Indicators",
     "Technical Indicators"])

with tab1:
    # Sidebar input for Share Prices tab
    with st.sidebar:
        symbol = st.text_input('Symbol', 'NVDA', key="share_symbol")
        function = st.selectbox('Function', ['TIME_SERIES_INTRADAY',
                                             'TIME_SERIES_DAILY',
                                             'TIME_SERIES_DAILY_ADJUSTED',
                                             'TIME_SERIES_WEEKLY',
                                             'TIME_SERIES_WEEKLY_ADJUSTED',
                                             'TIME_SERIES_MONTHLY',
                                             'TIME_SERIES_MONTHLY_ADJUSTED'], key="share_function")
        interval = st.selectbox('Interval', ['1min', '5min', '15min', '30min', '60min'], key="share_interval")
        data_type = st.selectbox('Data Type', ['json', 'csv'], key="share_data_type")
        output_size = st.selectbox('Output Size', ['compact', 'full'], key="share_output_size")
        extended = st.checkbox('Extended Hours', False, key="share_extended")
        api_key = st.text_input('API Key', 'demo', key="share_api_key")

    # Setting the title with the name of the symbol
    # st.title(f'{symbol.upper()} Share Prices')
    st.markdown(f"<span style='font-size: 18.3px;'>{symbol.upper()} Share Prices</span>", unsafe_allow_html=True)


    class APIRequest:
        @staticmethod
        @st.cache_data(ttl=600)  # Cache data for 10 minutes; adjust TTL as needed
        def get_data(url):
            """
            Fetch data from the constructed URL.
            :param url: The URL to fetch data from.
            :return: The response from the API.
            """
            response = requests.get(url, timeout=10)  # Timeout after 10 seconds
            return response.text

        def build_url(self):
            raise NotImplementedError("Subclass must implement abstract method")


    class AlphaVantageRequest(APIRequest):
        """Class for constructing requests to the Alpha Vantage API."""

        def __init__(self, symbol, function, interval, data_type, output_size, extended, api_key):
            self.symbol = symbol
            self.function = function
            self.interval = interval
            self.data_type = data_type
            self.output_size = output_size
            self.extended = extended  # This is now a boolean
            self.api_key = api_key

        def build_url(self):
            # Convert boolean to 'true'/'false' string
            extended_str = 'true' if self.extended else 'false'
            return (f'https://www.alphavantage.co/query'
                    f'?function={self.function}'
                    f'&symbol={self.symbol}'
                    f'&interval={self.interval}'
                    f'&datatype={self.data_type}'
                    f'&outputsize={self.output_size}'
                    f'&extended_hours={extended_str}'
                    f'&apikey={self.api_key}')


    # Fetch Data button
    if st.button('Fetch Data', key="share_fetch"):
        api_request = AlphaVantageRequest(
            symbol=symbol,
            function=function,
            interval=interval,
            data_type=data_type,
            output_size=output_size,
            extended=extended,
            api_key=api_key
        )
        url = api_request.build_url()
        data = APIRequest.get_data(url)

        # Display data
        if data_type == 'json':
            st.json(data)
        else:  # Assume CSV
            # Convert string data to DataFrame
            data_io = StringIO(data)  # Convert string to file-like object
            df = pd.read_csv(data_io)
            # Display the DataFrame as a table
            st.table(df)


def main():
    """
    Main function for the Streamlit app.
    :return: None
    """
    APIRequest()


if __name__ == "__main__":
    main()
