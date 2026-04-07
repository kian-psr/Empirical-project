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


API_KEY = "PASTE_YOUR_KEY_HERE"

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

ticker = "SPY"

url = (
    "https://www.alphavantage.co/query"
    f"?function=TIME_SERIES_DAILY_ADJUSTED"
    f"&symbol={ticker}"
    f"&outputsize=full"
    f"&datatype=csv"
    f"&apikey={API_KEY}"
)

response = requests.get(url, timeout=30)
response.raise_for_status()

output_file = RAW_DIR / f"{ticker}.csv"
output_file.write_bytes(response.content)

print(f"Saved {ticker} to {output_file}")