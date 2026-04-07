from pathlib import Path
from wsgiref.headers import Headers
import requests

# ETFs to download:
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

# The tickers to be used
TICKERS= ["SPY", "XLK", "XLF", "XLV", "XLE", "XLY", "XLU", "XLP", "XLB"]

# Folder where to save the raw data
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0"  # makes the request look like it comes from a normal browser
}

for ticker in TICKERS:
    # Stooq uses lower case tickers in the URL with .us for US ETFs
    stooq_symbol = f"{ticker.lower()}.us"
    BASE_URL = f"https://stooq.com/q/d/l/?s={stooq_symbol}&i=d"     #i=d means daily data

    print(f"Downloading {ticker} from {BASE_URL}...") # print which ticker is being downloaded and from which URL

    response = requests.get(BASE_URL, headers=HEADERS, timeout=70) # timeout of 70 seconds to avoid hanging indefinitely if the server is slow 
    response.raise_for_status() # check if the request was successful, if not it will raise an Error with the status code

    content = response.text.strip() # remove any whitespace from the response content

# Basic check so I do not save an error page as a CSV
    if not content:
        print(f"No data returned for {ticker}")
        continue

    first_line = content.splitlines()[0]
    if first_line != "Date,Open,High,Low,Close,Volume":
        print(f"Unexpected response for {ticker}")
        print(content[:200])
        continue

    output_file = RAW_DIR / f"{ticker}.csv"
    output_file.write_text(content, encoding="utf-8") # save the content to a CSV file in the raw data folder with UTF-8 encoding. 
    # UTF-8 is a common encoding that can handle a wide range of characters, ensuring that the data is saved correctly regardless of any special characters that may be present in the response.

    print(f"Saved {ticker} to {output_file}")

print("All data downloaded successfully!")