import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
portfolio = pd.read_csv("09_portfolio_holdings.csv")

# Group by sector
sector = portfolio.groupby("sector")["weight_pct"].sum()

plt.figure(figsize=(8,8))

plt.pie(
    sector,
    labels=sector.index,
    autopct="%1.1f%%",
    wedgeprops={"width":0.4},
    startangle=90
)

plt.title("Sector Allocation")

plt.show()