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
    if "timestamp" not in df.columns or "close" not in df.columns:
        print(f"Skipping {csv_file.name} because it does not have a timestamp or close column.")
        continue

    # only keep the columns we need
    df = df[["timestamp", "close"]].copy()

    # convert columns to the correct format
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    # remove any rows with missing values 
    df = df.dropna()

    #sort the data by timestamp in ascending order
    df = df.sort_values("timestamp")

    # add the ticker and sector name as new columns in the dataframe
    df["ticker"] = ticker
    df["sector"] = sector_name

    #store the cleaned dataframe in the list
    all_data.append(df)

# if no valid files were found, print a message
if not all_data:
    print("No valid CSV files were found in data/raw.")

else:
    # combine all cleaned dataframes into one dataset
    combined_df = pd.concat(all_data, ignore_index=True)

    # sort the final dataset by ticker and timestamp
    combined_df = combined_df.sort_values(["ticker", "timestamp"]).reset_index(drop=True)

    # save the cleaned dataset into the clean folder
    output_file = CLEAN_DIR / "sector_prices.csv"
    combined_df.to_csv(output_file, index=False)

    print(f"Saved cleaned data to {output_file}")
    print(combined_df.head())