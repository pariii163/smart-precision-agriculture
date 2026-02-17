import pandas as pd

file_path = "data/soil_datasets/RS_Session_257_AU_2256_1.csv"

df = pd.read_csv(file_path)

def compute_score(df, nutrient_prefix):
    vl = df[f"{nutrient_prefix} - VL"]
    l  = df[f"{nutrient_prefix} - L"]
    m  = df[f"{nutrient_prefix} - M"]
    h  = df[f"{nutrient_prefix} - H"]
    vh = df[f"{nutrient_prefix} - VH"]
    total = df["Total No. of Samples"]

    score = (1*vl + 2*l + 3*m + 4*h + 5*vh) / total
    return score

df_features = pd.DataFrame()
df_features["State/UT"] = df["State/UT"]

df_features["N_score"]  = compute_score(df, "Nitrogen (N)")
df_features["P_score"]  = compute_score(df, "Phosphorous (P)")
df_features["K_score"]  = compute_score(df, "Potassium (K)")
df_features["OC_score"] = compute_score(df, "Organic Carbon (OC)")

print("Aggregated feature dataset:")
print(df_features.head())

print("\nFeature statistics:")
print(df_features.describe())

output_path = "data/soil_datasets/shc_soil_features.csv"
df_features.to_csv(output_path, index=False)

print(f"\nSaved processed soil features to: {output_path}")

