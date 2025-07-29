import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry
from matplotlib.patches import Patch

COLORS = {
    "High income": "#003f5c",
    "Upper middle income": "#2f4b7c",
    "Lower middle income": "#f95d6a",
    "Low income": "#d45087",
}

file_path_pop = "./data/API_SP.POP.TOTL_DS2_en_csv_v2_38144.csv"
file_path_inc = "./data/Metadata_Country_API_SP.POP.TOTL_DS2_en_csv_v2_38144.csv"
df_raw_pop = pd.read_csv(file_path_pop, skiprows=4)
df_raw_inc = pd.read_csv(file_path_inc)



df_pop = df_raw_pop[["Country Name", "2022"]].dropna()
df_inc = df_raw_inc[["TableName", "IncomeGroup"]].dropna()

df_pop = df_pop.rename(columns={"Country Name": "Country", "2022": "Population"})
df_inc = df_inc.rename(columns={"TableName": "Country", "IncomeGroup": "IncomeGroup"})

df_pop["Verified_country"] = df_pop["Country"].str.strip().str.lower()
df_inc["Verified_country"] = df_inc["Country"].str.strip().str.lower()

verified_country = [country.name.lower() for country in pycountry.countries]
df_pop = df_pop[df_pop["Verified_country"].isin(verified_country)]
df_inc = df_inc[df_inc["Verified_country"].isin(verified_country)]

df_pop.drop(columns=["Verified_country"])
df_inc.drop(columns=["Verified_country"])


df_merged = pd.merge(df_pop, df_inc, on="Country")

df_merged["Population"] = pd.to_numeric(df_merged["Population"], errors="coerce")

df_merged = df_merged.sort_values(by="Population", ascending=False).head(50)

df_merged["Color"] = df_merged["IncomeGroup"].map(COLORS)


plt.figure(figsize=(16, 8))
bars = plt.bar(
    df_merged["Country"],
    df_merged["Population"],
    color=df_merged["Color"],
)

plt.xticks(rotation=90, fontsize=8)
plt.xlabel("Country")
plt.ylabel("Population (2022)")
plt.title("Population by Country and Income Group")

legend_handles = [Patch(color=color, label=label) for label, color in COLORS.items()]
plt.legend(handles=legend_handles, title="Income Group")

plt.tight_layout()
plt.show()

