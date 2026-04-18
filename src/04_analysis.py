import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np

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
# 1. Summary statistics table for each sector (Ticker)
#-----------------------------------------------------------------------------------------------------------------
summary_stats = (
    df.groupby("Ticker")["Daily Return (%)"]
    .agg(["mean", "std", "min", "max", "count"]) # Calculate mean, standard deviation, min, max and count of daily returns for each Ticker
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

# fixed colour map for all charts in the project
sector_colors = {
    "SPY": "#000000",  # black benchmark
    "XLK": "#4E79A7",  # blue
    "XLE": "#F28E2B",  # orange
    "XLB": "#5BD64B",  # green
    "XLY": "#FF0004",  # red
    "XLV": "#E478C6",  # purple
    "XLF": "#9C755F",  # brown
    "XLP": "#FFC800",  # yellow
    "XLU": "#85E9E1",  # teal
}
# sort data again just to make sure its in the right order
df = df.sort_values(["Ticker", "Date"]).reset_index(drop=True)

# Calculate the cumulative return for each Ticker. Growth if £1 invested
df ["cumulative return"] = (
    (1 + df["Daily Return (Decimal)"])
    .groupby(df["Ticker"])
    .cumprod() -1
)

# Get tickers ordered by final cumulative return, highest first
legend_order = (
    df.groupby("Ticker")["cumulative return"]
    .last()
    .sort_values(ascending=False)
    .index
)
# Plot the cumulative return for each sector
plt.figure(figsize=(12, 7))

for Ticker in legend_order:
    ticker_data = df[df["Ticker"] == Ticker]
    
    # Highlight SPY with a thicker line and different color to make it stand out as the benchmark
    if Ticker == "SPY":
        plt.plot(
            ticker_data["Date"], 
            ticker_data["cumulative return"], 
            label=Ticker, 
            linewidth=1.3, 
            color=sector_colors[Ticker],
        )
    else:
        plt.plot(
            ticker_data["Date"], 
            ticker_data["cumulative return"], 
            label=Ticker, 
            linewidth=0.8,
            alpha=0.7,
            color=sector_colors[Ticker],
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

#-----------------------------------------------------------------------------------------------------------------
# 2.1 Cumulative return figure for each sector during Covid-19 pandemic
#-----------------------------------------------------------------------------------------------------------------

# this is to calculate the cumulative return for each sector during the Covid-19 pandemic and plot it over time
# we will look at data from january 2020 to december 2023 to capture the full period of the pandemic and its aftermath

covid_df = df[(df["Date"] >= "2020-01-01") & (df["Date"] <= "2023-12-31")].copy()

# re-calculate the cumulative return for each ticker during the covid period to 0% begin with at the start of the period
covid_df["cumulative return"] = (
    (1 + covid_df["Daily Return (Decimal)"])
    .groupby(covid_df["Ticker"])
    .cumprod() -1
)

# Get tickers ordered by final cumulative return during the covid period, highest first
covid_legend_order = (
    covid_df.groupby("Ticker")["cumulative return"]
    .last()
    .sort_values(ascending=False)
    .index
)
# Plot the cumulative return for each sector during the covid period
fig, ax = plt.subplots(figsize=(13, 7.5))
for Ticker in covid_legend_order:
    ticker_data = covid_df[covid_df["Ticker"] == Ticker]
    
    # Highlight SPY with a thicker line and different color to make it stand out as the benchmark
    if Ticker == "SPY":
        plt.plot(
            ticker_data["Date"], 
            ticker_data["cumulative return"], 
            label=Ticker, 
            linewidth=1.8, 
            color=sector_colors[Ticker],
            zorder=3  # Ensure SPY is plotted on top of the other lines
        )

    else:
        plt.plot(
            ticker_data["Date"], 
            ticker_data["cumulative return"], 
            label=Ticker, 
            linewidth=1.1,
            alpha=0.6,
            color=sector_colors[Ticker],
            zorder=2  # Plot other sectors below SPY
        )

ax.set_title("Cumulative Returns of Sector ETFs & Benchmark (SPY) During Covid-19 Pandemic")
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Return")
plt.legend()    

ax.yaxis.set_major_formatter(PercentFormatter(1))  # Format y-axis as percentage

# add light horizontal grid lines
plt.grid(axis="y", linestyle="--", alpha=0.35)
plt.axhline(0, color="grey", linestyle="--", linewidth=0.8, alpha=0.7)  # Add a horizontal line at 0% to show the break-even point

ax.spines["top"].set_visible(False)  # Remove the top spine for a cleaner look
ax.spines["right"].set_visible(False)  # Remove the right spine for a cleaner look

# move the legend outside the plot area to the right
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))  
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_FIGURE / "cumulative_returns_covid.png")
plt.close()

print("Saved cumulative returns during Covid-19 figure.")


#-----------------------------------------------------------------------------------------------------------------
# 3. Correlation heatmap of daily returns 
#-----------------------------------------------------------------------------------------------------------------
# This is to calculate the correlation of daily returns between the different sectors and plot it as a heatmap

#keep only the necessary columns for the correlation calculation
corr_df = df[["Ticker", "Date", "Daily Return (%)"]].copy()

# pivot the data to have tickers as columns and dates as rows, with daily returns as values
corr_wide = corr_df.pivot(index="Date", columns="Ticker", values="Daily Return (%)")

# calculate the correlation matrix 
correlation_matrix = corr_wide.corr().round(3)

# save as table
correlation_matrix.to_csv(OUTPUT_TABLE / "correlation_matrix.csv")
print("Saved correlation matrix table.")

# plot the correlation matrix as a heatmap
plt.figure(figsize=(10, 8))
plt.imshow(correlation_matrix, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(label="Correlation Coefficient")
plt.xticks(ticks=np.arange(len(correlation_matrix.columns)), labels=correlation_matrix.columns, rotation=45)
plt.yticks(ticks=np.arange(len(correlation_matrix.index)), labels=correlation_matrix.index)

# add correlation values inside each cell
for i in range(len(correlation_matrix.index)):
    for j in range(len(correlation_matrix.columns)):
        plt.text(
            j,
            i,
            correlation_matrix.iloc[i, j],
            ha="center",
            va="center",
            color="black",
            fontsize=9
        )

plt.title("Correlation Heatmap of Daily Returns")
plt.tight_layout()

plt.savefig(OUTPUT_FIGURE / "correlation_heatmap.png")
plt.close() 

print("Saved correlation heatmap figure.")

#-----------------------------------------------------------------------------------------------------------------
# 4. Volatility comparison 
#-----------------------------------------------------------------------------------------------------------------

# this is to compare the volatility of the different sectors using a bar chart.
# we will use annulaised volatility for this
# the formula = daily volatility * sqrt(252) as 252 is the number of trading days in a year

# remove any rows if there are missing values in daily return again just to be sure
vol_df = df.dropna(subset=["Daily Return (%)"]) 

#calculate the annualized volatility for each Ticker and make a table
volatility_table = (
    vol_df.groupby("Ticker")["Daily Return (%)"]
    .std() * np.sqrt(252) # this calculates the standard deviation of daily returns for each Ticker and then annualizes it by multiplying by the square root of 252
    ).round(3).sort_values(ascending=False).reset_index(name="Annualized Volatility (%)") 

#save the volatility table to a csv file
volatility_table.to_csv(OUTPUT_TABLE / "volatility_table.csv", index=False)

print("Saved volatility table.")

# plot the volatility comparison as a bar chart
plt.figure(figsize=(10, 6))
colors = ["lightcoral" if Ticker == "SPY" else "skyblue" for Ticker in volatility_table["Ticker"]]
plt.bar(volatility_table["Ticker"], volatility_table["Annualized Volatility (%)"], color=colors)
plt.title("Annualized Volatility of Sector ETFs and Benchmark (SPY)") 
plt.xlabel("Ticker")
plt.ylabel("Annualized Volatility (%)")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.35)
plt.tight_layout()

plt.savefig(OUTPUT_FIGURE / "volatility_comparison.png")
plt.close()

print("Saved volatility comparison figure.")
