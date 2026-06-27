import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

cat = pd.read_csv("05_category_inflows.csv")

table = cat.pivot(
    index="category",
    columns="month",
    values="net_inflow_crore"
)

plt.figure(figsize=(14,6))

sns.heatmap(table,cmap="YlGnBu")

plt.title("Category Inflows")

plt.show()