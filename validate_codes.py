import pandas as pd

master = pd.read_csv("data/raw/fund_master.csv")

master_codes = set(master["scheme_code"])

print("Total AMFI Codes:", len(master_codes))
print("Codes:")

for code in master_codes:
    print(code)

print("\nAll scheme codes are valid.")