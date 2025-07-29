import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry

file_path = "./data/Task 1/API_SP.POP.TOTL_DS2_en_csv_v2_38144.csv"
df_raw = pd.read_csv(file_path, skiprows=4)



df = df_raw[["Country Name", "2022"]].dropna()
df = df.rename(columns={"Country Name": "Country", "2022": "Population"})
df["Verify_country"] = df["Country"].str.strip().str.lower()


verified_country = [country.name.lower() for country in pycountry.countries]

df = df[df["Verify_country"].isin(verified_country)]
df.drop(columns=["Verify_country"])

df_top = df.sort_values(by="Population", ascending=False).head(20)

plt.figure(figsize=(14, 8))
sns.barplot(data=df_top, y="Country", x="Population", palette="viridis")
plt.title("Top 20 Most Populous Countries (2022)", fontsize=16)
plt.xlabel("Population")
plt.ylabel("Country")
plt.grid(axis='x')
plt.tight_layout()
plt.show()
