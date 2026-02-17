import pandas as pd

file_path = "data/soil_datasets/RS_Session_257_AU_2256_1.csv"

df = pd.read_csv(file_path)

# Columns to keep (adjust names ONLY if spelling differs)
columns_to_keep = [
    "State/UT",
    "Total No. of Samples",

    "Nitrogen (N) - VL",
    "Nitrogen (N) - L",
    "Nitrogen (N) - M",
    "Nitrogen (N) - H",
    "Nitrogen (N) - VH",

    "Phosphorous (P) - VL",
    "Phosphorous (P) - L",
    "Phosphorous (P) - M",
    "Phosphorous (P) - H",
    "Phosphorous (P) - VH",

    "Potassium (K) - VL",
    "Potassium (K) - L",
    "Potassium (K) - M",
    "Potassium (K) - H",
    "Potassium (K) - VH",

    "Organic Carbon (OC) - VL",
    "Organic Carbon (OC) - L",
    "Organic Carbon (OC) - M",
    "Organic Carbon (OC) - H",
    "Organic Carbon (OC) - VH"
]

df_selected = df[columns_to_keep]

print("Selected dataset shape:", df_selected.shape)
print(df_selected.head())
