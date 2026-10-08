import requests
from datetime import datetime

# Your RapidAPI Key
API_KEY = 'Your_Key_Here'

# Function to fetch real-time data from Yahoo Finance via RapidAPI
def get_yahoo_finance_data(symbol):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes?symbols={symbol}®ion=US"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    # Check if the symbol was found and return the quote
    if "quoteResponse" in data and len(data["quoteResponse"]["result"]) > 0:
        return data["quoteResponse"]["result"][0]
    else:
        return None

# Function to print stock/index data
def print_yahoo_finance_data(symbol, data):
    if data:
        print(f"{symbol} Data:")
        print(f"Price: ${data['regularMarketPrice']}")
        print(f"Previous Close: ${data['regularMarketPreviousClose']}")
        print(f"Change: {data['regularMarketChange']} ({data['regularMarketChangePercent']}%)")
        print(f"Volume: {data['regularMarketVolume']}\n")
    else:
        print(f"No data found for {symbol}.\n")

# Fetch and print data for multiple symbols
def fetch_and_print_data():
    print(f"Fetching data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ET\n")

    # List of symbols to fetch
    symbols = ['^DJI', '^GSPC', '^IXIC', '^VIX', 'GC=F', 'CL=F', 'BTC-USD', '^TNX']

    # Fetch and print data for each symbol
    for symbol in symbols:
        data = get_yahoo_finance_data(symbol)
        print_yahoo_finance_data(symbol, data)

# Call the function to fetch and print data when the script is run

print(
    """
    Symbol Definitions:
    -------------------
    Dow Jones Industrial Average:  ^DJI
    S&P 500 Index:                 ^GSPC
    NASDAQ Composite Index:        ^IXIC
    Volatility Index (VIX):        ^VIX
    Gold Futures:                  GC=F
    WTI Crude Oil Futures:         CL=F
    Bitcoin (BTC) to USD:          BTC-USD
    10-Year Treasury Yield:        ^TNX
    """
)
fetch_and_print_data()
