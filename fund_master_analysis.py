import pandas as pd

df = pd.read_csv("data/raw/fund_master.csv")

print("Fund Houses:")
print(df["fund_house"].unique())

print("\nCategories:")
print(df["category"].unique())

print("\nSubcategories:")
print(df["subcategory"].unique())

print("\nRisk Grades:")
print(df["risk_grade"].unique())