import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
investor = pd.read_csv("08_investor_transactions.csv")

plt.figure(figsize=(8,5))

sns.boxplot(
    data=investor,
    x="age_group",
    y="amount_inr"
)

plt.title("Investment Amount by Age Group")

plt.show()