import pandas as pd

# Update filename if needed
file_path = "data/soil_datasets/RS_Session_257_AU_2256_1.csv"

df = pd.read_csv(file_path)

print("Dataset shape (rows, columns):")
print(df.shape)

print("\nColumn names:")
for col in df.columns:
    print(col)

print("\nFirst 5 rows:")
print(df.head())
