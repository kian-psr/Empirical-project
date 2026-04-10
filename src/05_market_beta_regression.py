import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import statsmodels.api as sm # this is to perform the regression analysis
import numpy as np

# Set file paths again
CLEAN_DIR = Path("data/clean")
OUTPUT_FIGURE = Path("output/figures")
OUTPUT_TABLE = Path("output/tables")

# Read the daily returns data
input_file = CLEAN_DIR / "sector_daily_returns.csv"
df = pd.read_csv(input_file)

# Check if the necessary columns are present again
if "Date" not in df.columns or "Daily Return (%)" not in df.columns:
    raise ValueError("The input file must contain 'Date' and 'Daily Return (%)' columns.")

# Keep only the necessary columns for the regression analysis
df = df[["Date", "ticker", "Daily Return (%)"]].copy()

# Convert the Date column to datetime format for plotting
df["Date"] = pd.to_datetime(df["Date"])

# split the data into a separate dataframe for the market (SPY) and the sectors
market_df = df[df["ticker"] == "SPY"].copy() # this is the dataframe for the market (SPY)
market_df = market_df.rename(columns={"Daily Return (%)": "Market Daily Return (%)"}) # rename the column to make it more clear

sectors_df = df[df["ticker"] != "SPY"].copy() # this is the dataframe for the sectors (everything except SPY)

# create an empty list to store the regression results
regression_results = []

# Run one regression for each sector etf
for ticker in sectors_df["ticker"].unique():
    sector_data = sectors_df[sectors_df["ticker"] == ticker].copy() # get the data for the current sector

    # Merge the sector data with the market data on the Date column to align the returns
    merged_data = pd.merge(sector_data, market_df, on="Date", how="inner")

    # Convert returns to numeric
    merged_data["Daily Return (%)"] = pd.to_numeric(merged_data["Daily Return (%)"], errors="coerce")
    merged_data["Market Daily Return (%)"] = pd.to_numeric(merged_data["Market Daily Return (%)"], errors="coerce")

    # Replace inf with NaN, then drop missing rows
    merged_data = merged_data.replace([np.inf, -np.inf], np.nan)
    merged_data = merged_data.dropna(subset=["Daily Return (%)", "Market Daily Return (%)"])

    # Check if we have enough data points for regression (at least 2)
    if len(merged_data) < 2:
        print(f"Not enough data for {ticker} to perform regression. Skipping.")
        continue

    # Prepare the independent variable (market return) and dependent variable (sector return)
    X = merged_data["Market Daily Return (%)"] # this is the independent variable (market return)
    y = merged_data["Daily Return (%)"] # this is the dependent variable (sector return)

    # Merge the sector data with the market data on the Date column to align the returns

    # Add a constant to the independent variable for the intercept in the regression
    X = sm.add_constant(X)

    # Fit the OLS regression model
    model = sm.OLS(y, X).fit()

    # Store the regression results in a dictionary
    result = {
        "ticker": ticker,
        "alpha": model.params["const"], # this is the intercept (alpha)
        "beta": model.params["Market Daily Return (%)"], # this is the slope (beta)
        "r_squared": model.rsquared, # this is the R-squared value of the regression
        "observations": int(model.nobs), # this is the number of observations used in the regression
        "p_value_alpha": model.pvalues["const"], # this is the p-value for alpha
        "p_value_beta": model.pvalues["Market Daily Return (%)"] # this is the p-value for beta
    }

    regression_results.append(result)

print("Regression analysis completed for all sectors.")

# Convert the regression results into a DataFrame for better presentation
regression_df = pd.DataFrame(regression_results)

# round the results to 3 decimal places for better readability
regression_df = regression_df.round({
    "alpha": 3,
    "beta": 3,
    "r_squared": 3,
    "p_value_alpha": 3,
    "p_value_beta": 3
})
# Save the regression results to a CSV file
regression_df.to_csv(OUTPUT_TABLE / "market_beta_regression_results.csv", index=False)  

print(f"Market beta regression results saved to {OUTPUT_TABLE / 'market_beta_regression_results.csv'}")

# sort the regression results by beta in descending order 
regression_df = regression_df.sort_values("beta", ascending=False).reset_index(drop=True)

# Make a beta chart
plt.figure(figsize=(10, 6))
plt.bar(regression_df["ticker"], regression_df["beta"], color="skyblue") #create a bar chart with the tickers on the x-axis and the beta values on the y-axis

plt.title("Market Beta for Each Sector ETF")
plt.xlabel("Sector ETF")
plt.ylabel("Beta")
plt.grid(axis="y", linestyle="--", alpha=0.35)
plt.axhline(1, color="red", linestyle="--", label="Market Beta = 1") # add a horizontal line at beta = 1 to show the market beta
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(OUTPUT_FIGURE / "market_beta_chart.png")
plt.close()
print(f"Market beta chart saved to {OUTPUT_FIGURE / 'market_beta_chart.png'}")


