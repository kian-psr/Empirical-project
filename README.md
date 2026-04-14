# Empirical-project

## Project question

How do equity (ETFs) sectors differ in returns, volatility, and sensitivity (β) to the overall market over the last 16 years?

## Blog post
The Blog is found on my github website under the link:\
https://kian-psr.github.io/Empirical-project/  

## Project overview

In this project i will compare major equity sectors using daily market data and ETFs. It examines sector performance (return), volatility, correlation, and market sensitivity using Python analysis.

## Repository structure

- data/raw contains original data
- data/clean contains cleaned datasets
- docs contains the rendered website files used for GitHub Pages
- output contains figures and tables
- report contains the final blog as a Quarto file
- src means **source code** and contains the main Python scripts used in the project
- .gitignore tells git what files to ignore, like unnecessary mac files

## Replication

To reproduce this project, run the python script in the `src` folder in order from `01` to `05`

### Required Packages:

This Project uses exclusively Python and the following libraries:

- ***pandas***:
  - Used for cleaning, reading, and combining the data
- ***numpy***:
  - Used for numerical calculations
- ***matplotlib***:
  - Used for creating charts and figures for visualisation
- ***yfinance***:
  - Open source program used to download the financial data from Yahoo Finance
- ***statsmodels***:
  - Used for the stats model and the regression

You can install them with the following command line:\
`python3 -m pip install pandas numpy matplotlib yfinance statsmodels`

### Flowchart of actions

```mermaid
flowchart LR
    A(Download Data) --> B(Save Raw Data)
    B --> C(Clean & Combine Data)
    C --> D(Save Clean Data)
    D --> E(Calculate Daily Returns)
    E --> F[Run Analysis]
    F --> G("cumulative_returns.png")
    F --> H("correlation_heatmap.png")
    F --> I("volatility_table.csv")
    F --> J("volatility_comparison.png")
    F --> K("market_beta_regression_results.csv")
    F --> L("market_beta_chart.png")
```

### Project Workflow

1.  `src/01_get_data.py`

This script downloads daily ETF and benchmark price data from Yahoo Finance using `yfinance`.

2.  `src/02_clean_data.py`

This script reads the raw ETF data and cleans it by:\
- keeping required price columns 
- removes lines with missing data 
- sort the data by date and tickers
- adds ticker & sector labels 
- saves data to `data/clean/sector_prices.csv`

3.  `src/03_daily_return_data.py`

This script calculates daily percentage returns for each ETF using the cleaned data. The output is saved to `data/clean/sector_daily_returns.csv`

4.  `src/04_analysis.py`

Produces the descriptive outputs and visualsation used in the project:\
- Summary statistics 
- Cumulative return figure 
- Volatility comparison 
- Correlation heat-map 
- These are saved in `output/tables` and `output/figures`

5.  `src/05_market_beta_regression.py`

This script runs a market model regression for each sector ETF using SPY as the market benchmark It saves the regression results table and the market beta figure in `output/tables` and `output/figures`

### Run Order

To get the project replicated you have to run the script in this order:

`python3 src/01_get_data.py`\
`python3 src/02_clean_data.py`\
`python3 src/03_daily_return_data.py`\
`python3 src/04_analysis.py`\
`python3 src/05_market_beta_regression.py`

## Output

The final project outputs are stored in `output/figures` for figures in .png format and `output/tables` for tables in .csv format.\
The final report is available on the GitHub Pages website linked above.


## Notes

#### Data Range

This project uses daily ETF data from 2010-01-01 to 2025-12-31\
This gives a wide range of historical data that provides a good  amount of data points for analysis, while also being recent enough.

#### Source of ETFs

- All ETFs come from [**State Street SPDR Family**](https://www.ssga.com/us/en/intermediary/capabilities/equities/sector-investing/sector-and-industry-etfs) to keep the sample consistent
- They are all U.S. based because the project uses SPY as a benchmark
- It keeps the analysis consistent as SPY is consistently used as a benchmark across different analysis

#### The tickers represent the following:

| Ticker | Full name & Link |
|------------|------------------------------------------------------------|
| SPY | [State Street® SPDR® S&P 500®](https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy) |
| XLK | [State Street® Technology Select Sector](https://www.ssga.com/us/en/intermediary/etfs/state-street-technology-select-sector-spdr-etf-xlk) |
| XLF | [State Street® Financial Select Sector](https://www.ssga.com/us/en/intermediary/etfs/state-street-financial-select-sector-spdr-etf-xlf) |
| XLV | [State Street® Health Care Select Sector](https://www.ssga.com/us/en/intermediary/etfs/state-street-health-care-select-sector-spdr-etf-xlv) |
| XLE | [State Street® Energy Select Sector](https://www.ssga.com/us/en/intermediary/etfs/state-street-energy-select-sector-spdr-etf-xle) |
| XLY | [State Street® Consumer Discretionary Select Sector](https://www.ssga.com/us/en/intermediary/etfs/state-street-consumer-discretionary-select-sector-spdr-etf-xly) |
| XLU | [State Street® Utilities Select Sector](https://www.ssga.com/us/en/intermediary/etfs/state-street-utilities-select-sector-spdr-etf-xlu) |
| XLP | [State Street® Consumer Staples Select Sector](https://www.ssga.com/us/en/intermediary/etfs/state-street-consumer-staples-select-sector-spdr-etf-xlp) |
| XLB | [State Street® Materials Select Sector](https://www.ssga.com/us/en/intermediary/etfs/state-street-materials-select-sector-spdr-etf-xlb) |