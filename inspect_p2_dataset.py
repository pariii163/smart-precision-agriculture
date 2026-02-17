import pandas as pd

file_path = "data/soil_datasets/crop_geo.csv"

df = pd.read_csv(file_path)

print("P2 Dataset Shape (rows, columns):")
print(df.shape)

print("\nColumn names:")
for col in df.columns:
    print(col)

print("\nFirst 5 rows:")
print(df.head())

print("\nBasic statistics (numeric columns):")
print(df.describe())
