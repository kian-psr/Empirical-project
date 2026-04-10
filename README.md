# Empirical-project

## Project question
How do equity (ETFs) sectors differ in returns, volatility, and sensitivity (\(\beta \)\) to the overall market?


## Project overview 
In this project i will compare major equity sectors using daily market data and ETFs. It examines sector performance (return), volatility, correlation, and market sensitivity using Python analysis.


## Repository structure
data/raw contains original data  
data/clean contains cleaned datasets  
output contains figures and tables  
report contains the final blog or Quarto file
src means **source code** and contains the main Python scripts used in the project
.gitignore tells git what files to ignore, like uncessairy mac files

## Replication
To reproduce this project, you have to run the script (src) in order from 01 to 05

### Required Packages:
This Project uses exclusivley Python and the following libaries:

- pandas:
    - Used for cleaning, reading, and combining the data
    - I used them to wokr with the CSV files and caluclating returns
- numpy:
    - Used for nmumerical calculations
- matplotlib:
    - Used for creating charts and figures for visulaisation
- seaborn:
    - Used for more visual outputs like the heatmap 
- yfinance:
    - Open source program that I used to download the financial data from Yahoo Finance
- statsmodels:
    - Used for the stats model and the regression 

You can install them with the following command line: 
`python3 -m pip install pandas numpy matplotlib seaborn yfinance statsmodels`

### Project Workflow

#### Flowchart

```{mermaid}
flowchart LR
    A(Download Data) --> B(Save Raw Data)
    B --> C(Clean Data)
    C --> D(Save Clean Data)
    D --> E(Use Clean Data for Analysis)
    E --> F[Get Output]
    F --> G(cumulative_return.png)
    F --> H(correlation_heatmap.png)
    F --> I(volatility_table.csv)
    F --> J(volatility_comparison.png)
    F --> K(market_beta_regression_result.csv)
    F --> L(market_beta_chart.png)


```

1. `src/01_get_data.py`
This script is to download daily ETF aswell as market (SPY) price data from Yahoo Finance using yfinance for the the last 10 years using an interval of 1 day

