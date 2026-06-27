import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
nav = pd.read_csv("02_nav_history.csv")

# Convert date
nav["date"] = pd.to_datetime(nav["date"])

# Pivot table
pivot = nav.pivot(
    index="date",
    columns="amfi_code",
    values="nav"
)

# Daily returns
returns = pivot.pct_change()

# Select first 10 funds
returns = returns.iloc[:, :10]

# Correlation
corr = returns.corr()

plt.figure(figsize=(10,8))

sns.heatmap(
    corr,
    cmap="coolwarm",
    annot=True
)

plt.title("NAV Return Correlation Matrix")

plt.tight_layout()

plt.show()