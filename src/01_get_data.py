from pathlib import Path
import requests

# Donwload the data from alphavantage API
# Tickers I will use: SPY, XLK, XLF, XLV, XLE, XLY, XLU, XLP, XLB,

#-----------------------------------------
# SPY = the overall market benchmark
# XLK = technology
# XLF = financials
# XLV = health care
# XLE = energy
# XLY = consumer discretionary
# XLU = utilities
# XLP = consumer staples
# XLB = materials
#-----------------------------------------

# Insert your API key here which you can get for free on th website https://www.alphavantage.co/support/#api-key
API_KEY = "YOUR_API_KEY_HERE"

# you can change the function to get different data, for example TIME_SERIES_INTRADAY, TIME_SERIES_WEEKLY, TIME_SERIES_MONTHLY...
FUNCTION = "TIME_SERIES_DAILY"

# These are the tickers for the sectors ETFs.
TICKERS= ["SPY", "XLK", "XLF", "XLV", "XLE", "XLY", "XLU", "XLP", "XLB"]

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://www.alphavantage.co/query"

for ticker in TICKERS:
    params = {
        "function": FUNCTION,
        "symbol": ticker,
        "outputsize": "compact",  # you can change to "full" if you have premium
        "datatype": "csv",
        "apikey": API_KEY,  
    }

    print(f"Downloading data for {ticker} from Alpha Vantage...")


    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    output_file = RAW_DIR / f"{ticker}.csv"
    output_file.write_bytes(response.content)

    print(f"Saved {ticker} to {output_file}")

print("All data downloaded successfully!")