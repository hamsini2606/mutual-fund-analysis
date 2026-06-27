import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
folio = pd.read_csv("06_industry_folio_count.csv")

# Convert month column
folio["month"] = pd.to_datetime(folio["month"])

plt.figure(figsize=(12,5))

plt.plot(
    folio["month"],
    folio["total_folios_crore"],
    marker="o"
)

plt.title("Industry Folio Growth")
plt.xlabel("Month")
plt.ylabel("Total Folios (Crore)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()