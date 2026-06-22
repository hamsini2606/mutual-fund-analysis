import pandas as pd
import os

path = "data/raw"

files = [f for f in os.listdir(path) if f.endswith(".csv")]

for file in files:
    print("\n" + "="*50)
    print(file)

    df = pd.read_csv(os.path.join(path, file))

    print("\nShape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())