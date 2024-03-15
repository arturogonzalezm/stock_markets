import requests

SYMBOL = 'NVDA'
FUNCTION = 'TIME_SERIES_INTRADAY'
INTERVAL = '1min'
MONTH = '2024-03'
API_KEY = 'demo'
DATA_TYPE = 'csv'
OUTPUT_SIZE = 'full'
EXTENDED = 'true'


URL = (f'https://www.alphavantage.co/query'
       f'?function={FUNCTION}'
       f'&symbol={SYMBOL}'
       f'&interval={INTERVAL}'
       f'&month={MONTH}'
       f'&datatype={DATA_TYPE}'
       f'&outputsize={OUTPUT_SIZE}'
       f'&extended_hours={EXTENDED}'
       f'&apikey={API_KEY}')

response = requests.get(URL)
data = response.text
print(data)
