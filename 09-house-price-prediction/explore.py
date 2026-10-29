import pandas as pd

df = pd.read_csv("housing.csv")

print(df.shape)
print(df.head(3).T)
print()
print(df.isna().sum())
print()
print(df["ocean_proximity"].value_counts())
print()
print(df["median_house_value"].describe().round(0))
print("capped at 500,001:", (df["median_house_value"] == 500001).sum())
