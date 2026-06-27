import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

aum = pd.read_csv("03_aum_by_fund_house.csv")

plt.figure(figsize=(12,6))

sns.barplot(
    data=aum,
    x="fund_house",
    y="aum_lakh_crore",
    hue="date"
)

plt.xticks(rotation=90)
plt.title("AUM by Fund House")

plt.tight_layout()
plt.show()