import os

print("Current Working Directory:")
print(os.getcwd())

print("\nFiles in current directory:")
print(os.listdir())

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# =====================================
# Load Datasets
# =====================================

fund_master = pd.read_csv("data/01_fund_master.csv")

nav = pd.read_csv("data/02_nav_history.csv")

aum = pd.read_csv("data/03_aum_by_fund_house.csv")

sip = pd.read_csv("data/04_monthly_sip_inflows.csv")

category = pd.read_csv("data/05_category_inflows.csv")

folio = pd.read_csv("data/06_industry_folio_count.csv")

performance = pd.read_csv("data/07_scheme_performance.csv")

transactions = pd.read_csv("data/08_investor_transactions.csv")

holdings = pd.read_csv("data/09_portfolio_holdings.csv")

benchmark = pd.read_csv("data/10_benchmark_indices.csv")
# =====================================
# Convert Dates
# =====================================

nav["date"] = pd.to_datetime(nav["date"])

benchmark["date"] = pd.to_datetime(benchmark["date"])
# =====================================
# Sort NAV History
# =====================================

nav = nav.sort_values(
    ["amfi_code", "date"]
)
print(nav.head())

print(nav.shape)

print(nav.info())
# =====================================
# DAILY RETURNS
# =====================================

print("\nCalculating Daily Returns...")

# Calculate daily returns for each fund
nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
       .pct_change()
)

# Display first few rows
print(nav.head(10))

# Remove first NaN return for each fund
daily_returns = nav.dropna(subset=["daily_return"]).copy()

print("\nDaily Returns Shape:")
print(daily_returns.shape)

# Save the result
daily_returns.to_csv(
    "outputs/daily_returns.csv",
    index=False
)

print("\nDaily returns saved successfully!")
# =====================================
# CAGR CALCULATION
# =====================================

print("\nCalculating CAGR...")

TRADING_DAYS = 252


def calculate_cagr(nav_series, years):
    """
    Calculate CAGR for a fund over the specified number of years.
    Returns NaN if there is insufficient data.
    """

    required_days = years * TRADING_DAYS

    nav_series = nav_series.dropna()

    if len(nav_series) < required_days:
        return np.nan

    start_nav = nav_series.iloc[-required_days]
    end_nav = nav_series.iloc[-1]

    cagr = ((end_nav / start_nav) ** (1 / years)) - 1

    return cagr


# Store results
cagr_results = []

# Calculate CAGR for every fund
for fund in nav["amfi_code"].unique():

    fund_data = (
        nav[nav["amfi_code"] == fund]
        .sort_values("date")
    )

    nav_series = fund_data["nav"]

    cagr_1 = calculate_cagr(nav_series, 1)
    cagr_3 = calculate_cagr(nav_series, 3)
    cagr_5 = calculate_cagr(nav_series, 5)

    cagr_results.append({
        "amfi_code": fund,
        "1Y_CAGR": cagr_1,
        "3Y_CAGR": cagr_3,
        "5Y_CAGR": cagr_5
    })

# Convert to DataFrame
cagr_df = pd.DataFrame(cagr_results)

# Convert to percentages
cagr_df["1Y_CAGR_%"] = cagr_df["1Y_CAGR"] * 100
cagr_df["3Y_CAGR_%"] = cagr_df["3Y_CAGR"] * 100
cagr_df["5Y_CAGR_%"] = cagr_df["5Y_CAGR"] * 100

# Sort by 3-Year CAGR
cagr_df = cagr_df.sort_values(
    by="3Y_CAGR_%",
    ascending=False
)

# Display
print("\nTop Funds by 3-Year CAGR")
print(cagr_df.head(10))

# Save CSV
cagr_df.to_csv(
    "outputs/cagr_comparison.csv",
    index=False
)

print("\nCAGR Comparison Saved Successfully!")
# =====================================
# SHARPE RATIO
# =====================================

print("\nCalculating Sharpe Ratio...")

RISK_FREE_RATE = 0.065

sharpe_results = []

# Calculate Sharpe Ratio for each fund
for fund in daily_returns["amfi_code"].unique():

    fund_returns = (
        daily_returns[daily_returns["amfi_code"] == fund]["daily_return"]
        .dropna()
    )

    # Annualized Return
    annual_return = fund_returns.mean() * 252

    # Annualized Volatility
    annual_volatility = fund_returns.std() * np.sqrt(252)

    # Avoid division by zero
    if annual_volatility == 0:
        sharpe = np.nan
    else:
        sharpe = (annual_return - RISK_FREE_RATE) / annual_volatility

    sharpe_results.append({
        "amfi_code": fund,
        "Annual_Return": annual_return,
        "Annual_Volatility": annual_volatility,
        "Sharpe_Ratio": sharpe
    })

# Convert to DataFrame
sharpe_df = pd.DataFrame(sharpe_results)

# Rank funds
sharpe_df["Sharpe_Rank"] = sharpe_df["Sharpe_Ratio"].rank(
    ascending=False,
    method="dense"
)

# Sort by Sharpe Ratio
sharpe_df = sharpe_df.sort_values(
    by="Sharpe_Ratio",
    ascending=False
)

print("\nTop 10 Funds by Sharpe Ratio")
print(sharpe_df.head(10))

# Save CSV
sharpe_df.to_csv(
    "outputs/sharpe_ratio.csv",
    index=False
)

print("\nSharpe Ratio saved successfully!")
# =====================================
# SORTINO RATIO
# =====================================

print("\nCalculating Sortino Ratio...")

RISK_FREE_RATE = 0.065

sortino_results = []

for fund in daily_returns["amfi_code"].unique():

    fund_returns = (
        daily_returns[daily_returns["amfi_code"] == fund]["daily_return"]
        .dropna()
    )

    # Annual Return
    annual_return = fund_returns.mean() * 252

    # Downside Returns (only negative returns)
    downside_returns = fund_returns[fund_returns < 0]

    # Downside Volatility
    downside_std = downside_returns.std() * np.sqrt(252)

    if downside_std == 0 or np.isnan(downside_std):
        sortino = np.nan
    else:
        sortino = (annual_return - RISK_FREE_RATE) / downside_std

    sortino_results.append({
        "amfi_code": fund,
        "Annual_Return": annual_return,
        "Downside_Volatility": downside_std,
        "Sortino_Ratio": sortino
    })

# Convert to DataFrame
sortino_df = pd.DataFrame(sortino_results)

# Rank funds
sortino_df["Sortino_Rank"] = sortino_df["Sortino_Ratio"].rank(
    ascending=False,
    method="dense"
)

# Sort
sortino_df = sortino_df.sort_values(
    by="Sortino_Ratio",
    ascending=False
)

print("\nTop 10 Funds by Sortino Ratio")
print(sortino_df.head(10))

# Save CSV
sortino_df.to_csv(
    "outputs/sortino_ratio.csv",
    index=False
)

print("\nSortino Ratio saved successfully!")
# =====================================
# MODULE 6 : ALPHA & BETA
# =====================================

print("\nCalculating Alpha & Beta...")

# Keep only NIFTY100 benchmark
nifty100 = benchmark[benchmark["index_name"] == "NIFTY100"].copy()

nifty100["date"] = pd.to_datetime(nifty100["date"])

nifty100 = nifty100.sort_values("date")

# Benchmark daily returns
nifty100["benchmark_return"] = nifty100["close_value"].pct_change()

alpha_beta_results = []

for fund in daily_returns["amfi_code"].unique():

    fund_df = daily_returns[
        daily_returns["amfi_code"] == fund
    ][["date","daily_return"]]

    merged = pd.merge(
        fund_df,
        nifty100[["date","benchmark_return"]],
        on="date",
        how="inner"
    ).dropna()

    if len(merged) < 30:
        continue

    slope, intercept, r_value, p_value, std_err = linregress(
        merged["benchmark_return"],
        merged["daily_return"]
    )

    alpha_beta_results.append({
        "amfi_code": fund,
        "Alpha": intercept * 252,
        "Beta": slope,
        "R_squared": r_value**2
    })

alpha_beta_df = pd.DataFrame(alpha_beta_results)

alpha_beta_df = alpha_beta_df.sort_values(
    "Alpha",
    ascending=False
)

print(alpha_beta_df.head())

alpha_beta_df.to_csv(
    "outputs/alpha_beta.csv",
    index=False
)

print("\nAlpha Beta saved successfully!")
# =====================================
# MODULE 7 : MAXIMUM DRAWDOWN
# =====================================

print("\nCalculating Maximum Drawdown...")

drawdown_results = []

for fund in nav["amfi_code"].unique():

    fund_df = (
        nav[nav["amfi_code"] == fund]
        .sort_values("date")
    )

    running_max = fund_df["nav"].cummax()

    drawdown = fund_df["nav"] / running_max - 1

    max_dd = drawdown.min()

    end_date = fund_df.loc[
        drawdown.idxmin(),
        "date"
    ]

    start_date = fund_df.loc[
        fund_df["nav"][:drawdown.idxmin()].idxmax(),
        "date"
    ]

    drawdown_results.append({
        "amfi_code": fund,
        "Maximum_Drawdown": max_dd,
        "Start_Date": start_date,
        "End_Date": end_date
    })

drawdown_df = pd.DataFrame(drawdown_results)

drawdown_df = drawdown_df.sort_values(
    "Maximum_Drawdown"
)

print(drawdown_df.head())

drawdown_df.to_csv(
    "outputs/maximum_drawdown.csv",
    index=False
)

print("\nMaximum Drawdown saved!")
# =====================================
# MODULE 8 : FUND SCORECARD
# =====================================

print("\nGenerating Fund Scorecard...")

# Merge calculated alpha with performance data
score_df = performance.merge(
    alpha_beta_df[["amfi_code", "Alpha"]],
    on="amfi_code",
    how="left"
)

# Merge calculated max drawdown
score_df = score_df.merge(
    drawdown_df[["amfi_code", "Maximum_Drawdown"]],
    on="amfi_code",
    how="left"
)

# Merge calculated sharpe ratio
score_df = score_df.merge(
    sharpe_df[["amfi_code", "Sharpe_Ratio"]],
    on="amfi_code",
    how="left"
)

# Rank metrics
score_df["return_rank"] = score_df["return_3yr_pct"].rank(ascending=False)
score_df["sharpe_rank"] = score_df["Sharpe_Ratio"].rank(ascending=False)
score_df["alpha_rank"] = score_df["Alpha"].rank(ascending=False)

# Lower expense ratio is better
score_df["expense_rank"] = score_df["expense_ratio_pct"].rank(ascending=True)

# Smaller drawdown is better
score_df["drawdown_rank"] = score_df["Maximum_Drawdown"].rank(ascending=False)

# Composite score
score_df["Fund_Score"] = (
    0.30 * score_df["return_rank"] +
    0.25 * score_df["sharpe_rank"] +
    0.20 * score_df["alpha_rank"] +
    0.15 * score_df["expense_rank"] +
    0.10 * score_df["drawdown_rank"]
)

# Convert to 0–100
score_df["Fund_Score"] = (
    (score_df["Fund_Score"].max() - score_df["Fund_Score"]) /
    (score_df["Fund_Score"].max() - score_df["Fund_Score"].min())
) * 100

score_df = score_df.sort_values(
    "Fund_Score",
    ascending=False
)

print(score_df[
    ["scheme_name", "Fund_Score"]
].head(10))

score_df.to_csv(
    "outputs/fund_scorecard.csv",
    index=False
)

print("\nFund Scorecard saved successfully!")
# =====================================
# MODULE 9 : BENCHMARK COMPARISON
# =====================================

print("\nGenerating Benchmark Comparison...")

top5 = score_df.head(5)["amfi_code"]

tracking_results = []

plt.figure(figsize=(14,7))

# NIFTY100
benchmark_plot = benchmark[
    benchmark["index_name"] == "NIFTY100"
].copy()

benchmark_plot = benchmark_plot.sort_values("date")

benchmark_plot["normalized"] = (
    benchmark_plot["close_value"] /
    benchmark_plot["close_value"].iloc[0]
)

plt.plot(
    benchmark_plot["date"],
    benchmark_plot["normalized"],
    linewidth=3,
    label="NIFTY100"
)

for fund in top5:

    fund_nav = nav[
        nav["amfi_code"] == fund
    ].copy()

    fund_nav = fund_nav.sort_values("date")

    fund_nav["normalized"] = (
        fund_nav["nav"] /
        fund_nav["nav"].iloc[0]
    )

    plt.plot(
        fund_nav["date"],
        fund_nav["normalized"],
        label=str(fund)
    )

    fund_nav["fund_return"] = fund_nav["nav"].pct_change()

    merged = pd.merge(
        fund_nav[["date","fund_return"]],
        nifty100[["date","benchmark_return"]],
        on="date"
    ).dropna()

    tracking_error = (
        (merged["fund_return"] - merged["benchmark_return"]).std()
        * np.sqrt(252)
    )

    tracking_results.append({
        "amfi_code": fund,
        "Tracking_Error": tracking_error
    })

plt.title("Top 5 Funds vs NIFTY100")

plt.xlabel("Date")

plt.ylabel("Normalized NAV")

plt.legend()

plt.grid(True)

plt.savefig(
    "outputs/benchmark_comparison.png",
    dpi=300
)

plt.close()

tracking_df = pd.DataFrame(tracking_results)

tracking_df.to_csv(
    "outputs/tracking_error.csv",
    index=False
)

print("\nBenchmark comparison completed!")
# =====================================
# MODULE 10 : PROJECT SUMMARY
# =====================================

print("\n" + "="*60)
print(" MUTUAL FUND PERFORMANCE ANALYTICS COMPLETED ")
print("="*60)

print("\nGenerated Files:")

print("✔ daily_returns.csv")
print("✔ cagr_comparison.csv")
print("✔ sharpe_ratio.csv")
print("✔ sortino_ratio.csv")
print("✔ alpha_beta.csv")
print("✔ maximum_drawdown.csv")
print("✔ fund_scorecard.csv")
print("✔ tracking_error.csv")
print("✔ benchmark_comparison.png")

print("\nProject Completed Successfully!")