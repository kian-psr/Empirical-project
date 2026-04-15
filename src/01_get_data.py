from pathlib import Path
import yfinance as yf

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

# The range of data is from 2010 to 2025 which gives 15 years of data, this gives a lot of historic data to work with

START_DATE = "2010-01-01"
END_DATE = "2025-12-31"

for ticker in TICKERS:
    print(f"Downloading data for {ticker} from yfinance...")

    df= yf.download(
        ticker, 
        start=START_DATE, 
        end=END_DATE,
        interval="1d",  # Daily data
        auto_adjust=False, # keeps yahoo's normal columns including Adj Close which is what we will use for our analysis. If we set this to True, it will adjust the Close price for dividends and stock splits, which we don't want for our analysis.
        actions=False, # Exclude dividends and stock splits from the data.
        progress=False, # Disable the progress bar for cleaner output.
        threads=False, # Disable multithreading to avoid potential issues with large downloads.
        timeout=30, # Set a timeout for the download to prevent hanging.
    )
# skip if no data is found for the ticker
    if df.empty:
        print(f"No data found for {ticker}")
        continue

# Flatten the columns as yfinance returns a MultiIndex
    if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)

# Give the index a proper name so it saves as Date
    df.index.name = "Date"

# Save the data to a CSV file in the raw data directory.
    output_file = RAW_DIR / f"{ticker}.csv"
    df.to_csv(output_file)

    print(f"Saved {ticker} to {output_file}")

print("All data downloaded successfully!")