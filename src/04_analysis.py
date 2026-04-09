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
summary_stats = (
    df.groupby("ticker")["Daily Return (%)"]
    .agg(["mean", "std", "min", "max", "count"]) # Calculate mean, standard deviation, min, max and count of daily returns for each ticker
    .round(3)  # Round the statistics to 3 decimal places for better readability
    .reset_index() 
)
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
# 2. Cumulative return figure for each sector
#-----------------------------------------------------------------------------------------------------------------
# this is to calculate the cumulative return for each sector and plot it over time

# turn percent into decimal for the calulation of cumulative return
df["Daily Return (Decimal)"] = df["Daily Return (%)"] / 100

# Calculate the cumulative return for each ticker. Growth if £1 invested

df ["cumulative return"] = (
    (1 + df["Daily Return (Decimal)"])
    .groupby(df["ticker"])
    .cumprod() -1
)

# Plot the cumulative return for each sector
plt.figure(figsize=(12, 7))

for ticker in df["ticker"].unique():
    ticker_data = df[df["ticker"] == ticker]
    plt.plot(ticker_data["Date"], ticker_data["cumulative return"], label=ticker)

plt.title("Cumulative Returns of Sector ETFs & Benchmark (SPY)")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(OUTPUT_FIGURE / "cumulative_returns.png")
plt.close()

print("Saved cumulative returns figure.")
