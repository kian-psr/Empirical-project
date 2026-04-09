import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt

# Set file paths again
CLEAN_DIR = Path("data/clean")

OUTPUT_FIGURE = Path("output/figures")
OUTPUT_FIGURE.mkdir(parents=True, exist_ok=True)  # Create a folder for output figures inside output

OUTPUT_TABLE = Path("output/tables")
OUTPUT_TABLE.mkdir(parents=True, exist_ok=True)  # Create a folder for output tables inside output

# Read the daily returns data
df = pd.read_csv(CLEAN_DIR / "sector_daily_returns.csv")

# Check if the necessary columns are present
if "Date" not in df.columns or "Daily Return (%)" not in df.columns:
    print(f"Error: The input file must contain 'Date' and 'Daily Return (%)' columns.")

#-----------------------------------------------------------------------------------------------------------------
# 1. Summary statistics table for each sector (ticker)
#-----------------------------------------------------------------------------------------------------------------
summary_stats = df.groupby("ticker")["Daily Return (%)"].agg(["mean", "std", "min", "max", "count"]).reset_index()
summary_stats = summary_stats.round(3)  # Round the statistics to 3 decimal places for better readability

summary_stats = summary_stats.rename(columns={
    "mean": "Mean Daily Return (%)",
    "std": "Volatility (Std Dev)",
    "min": "Worst Daily Return (%)",
    "max": "Best Daily Return (%)",
    "count": "Total Observations"
})

summary_stats.to_csv(OUTPUT_TABLE / "summary_statistics.csv", index=False)

print(f"Summary statistics saved to {OUTPUT_TABLE / 'summary_statistics.csv'}")

print("Saved summary statistics table.")
#-----------------------------------------------------------------------------------------------------------------