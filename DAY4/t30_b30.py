import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
investor = pd.read_csv("08_investor_transactions.csv")

# Count city tiers
tier = investor["city_tier"].value_counts()

plt.figure(figsize=(6,6))

plt.pie(
    tier,
    labels=tier.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("T30 vs B30 City Tier")

plt.show()