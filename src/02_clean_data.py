from pathlib import Path
import pandas as pd 

RAW_DIR = Path("data/raw")  # This is the directory where the raw data is stored
CLEAN_DIR = Path("data/clean")  # This is the directory where the cleaned data will be stored

CLEAN_DIR.mkdir(parents=True, exist_ok=True)  # Create the clean directory if it doesn't exist

#convert the ticker names into clear sector names

ticker_to_sector = {
    "SPY": "Overall Market",
    "XLK": "Technology",
    "XLF": "Financials",
    "XLV": "Health Care",
    "XLE": "Energy",
    "XLY": "Consumer Discretionary",
    "XLU": "Utilities",
    "XLP": "Consumer Staples",
    "XLB": "Materials"
}   

# create an empty list to store the cleaned dataframes§
all_data = []

#loop through each csv file in the raw directory, clean it and save it to the clean directory
for csv_file in RAW_DIR.glob("*.csv"):
    ticker = csv_file.stem  # Get the ticker from the file name
    sector_name = ticker_to_sector.get(ticker, "Unknown Sector")  # Get the sector name from the ticker

    # Read the raw data
    df = pd.read_csv(csv_file)

    #look if it has a timestamp column and if it does not skip it
    if "timestamp" not in df.columns:
        print(f"Skipping {csv_file} because it does not have a timestamp column.")
        continue

    #only keep the column we need
    #timestamp for date and close for daily price
    df = df[["timestamp", "close"]].copy()

    # change the close column into a numeric format 
    # if there are any non-numeric or missing values, they will be converted to NaN
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    # remove any rows with missing values 
    df = df.dropna()

    #sort the data by timestamp in ascending order
    df = df.sort_values("timestamp")



