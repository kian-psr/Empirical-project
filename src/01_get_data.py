from pathlib import Path
import yfinance as yf
import requests

# Use yfinance to get the data for the sector ETFs. 
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
TICKERS= ["SPY", "XLK", "XLF", "XLV", "XLE", "XLY", "XLU", "XLP", "XLB"]

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# tickers = yf.download(TICKERS, start="2010-01-01", end="2024-01-01", group_by='ticker')
for ticker in TICKERS:
    print(f"Downloading data for {ticker} from yfinance...")

    df= yf.download(
        ticker, 
        period="5y", # Download data for the last 5 years.
        interval="1d",  # Daily data
        auto_adjust=False, # Adjusted Close price, which accounts for corporate actions like dividends and stock splits.
        actions=False, # Exclude dividends and stock splits from the data.
        progress=False, # Disable the progress bar for cleaner output.
        threads=False, # Disable multithreading to avoid potential issues with large downloads.
        timeout=30, # Set a timeout for the download to prevent hanging.
    )
# skip if no data is found for the ticker
    if df.empty:
        print(f"No data found for {ticker}")
        continue

# Save the data to a CSV file in the raw data directory.
    output_file = RAW_DIR / f"{ticker}.csv"
    df.to_csv(output_file)

    print(f"Saved {ticker} to {output_file}")

print("All data downloaded successfully!")