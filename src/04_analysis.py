import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter

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

# convert the Date column to datetime format for plotting
df["Date"] = pd.to_datetime(df["Date"])

# sort fdata again just to make sure its in the right order
df = df.sort_values(["ticker", "Date"]).reset_index(drop=True)

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
    
    # Highlight SPY with a thicker line and different color to make it stand out as the benchmark
    if ticker == "SPY":
        plt.plot(
            ticker_data["Date"], 
            ticker_data["cumulative return"], 
            label=ticker, 
            linewidth=2.8, 
            color="black"
        )
    else:
        plt.plot(
            ticker_data["Date"], 
            ticker_data["cumulative return"], 
            label=ticker, 
            linewidth=1.8
        )
    


plt.title("Cumulative Returns of Sector ETFs & Benchmark (SPY)")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()

plt.gca().yaxis.set_major_formatter(PercentFormatter(1))  # Format y-axis as percentage

# add light horizontal grid lines
plt.grid(axis="y", linestyle="--", alpha=0.35)

# move the legend outside the plot area to the right
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(OUTPUT_FIGURE / "cumulative_returns.png")
plt.close()

print("Saved cumulative returns figure.")
