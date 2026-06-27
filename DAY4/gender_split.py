import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
investor = pd.read_csv("08_investor_transactions.csv")

# Count gender
gender = investor["gender"].value_counts()

# Plot
plt.figure(figsize=(6,6))

plt.pie(
    gender,
    labels=gender.index,
    autopct="%1.1f%%"
)

plt.title("Gender Split")

plt.show()
gender = investor["gender"].value_counts()

plt.figure(figsize=(6,6))

plt.pie(
    gender,
    labels=gender.index,
    autopct="%1.1f%%"
)

plt.title("Gender Split")

plt.show()