# This is to calculate the daily return in % for all tickers and days

import pandas as pd
from pathlib import Path

# Set file paths again
CLEAN_DIR = Path("data/clean")
INPUT_FILE = CLEAN_DIR / "sector_prices.csv"
OUTPUT_FILE = CLEAN_DIR / "sector_daily_returns.csv"

# Read the sectore price data
df = pd.read_csv(INPUT_FILE)

# Check if the necessary columns are present
if "Date" not in df.columns or "Adj Close" not in df.columns:
    print(f"Error: The input file must contain 'Date' and 'Adj Close' columns.")

# Sort by ticker and date just to be sure before calculating returns
df = df.sort_values(["ticker", "Date"]).reset_index(drop=True)

# Calculate the daily return in percentage
# The formula for daily return is: (Current Day's Price - Previous Day's Price) / Previous Day's Price * 100
df["Daily Return (%)"] = df.groupby("ticker")["Adj Close"].pct_change() * 100 # this calculates the percentage change in the Adj Close price for each ticker, which gives us the daily return in percentage and its all seperated by ticker.
df["Daily Return (%)"] = df["Daily Return (%)"].round(3) # this rounds the daily return to 3 decimal places

# Save the results to a new CSV file
df.to_csv(OUTPUT_FILE, index=False)

# Print a message to show it worked
print(f"Daily returns calculated and saved to {OUTPUT_FILE}")