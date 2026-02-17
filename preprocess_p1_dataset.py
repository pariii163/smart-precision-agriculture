import pandas as pd
from sklearn.preprocessing import MinMaxScaler

file_path = "data/soil_datasets/crop_recommendation.csv"

df = pd.read_csv(file_path)

# Select core soil features and target
features = ["N", "P", "K"]
target = "label"

X = df[features]
y = df[target]

# Normalize N, P, K
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

df_processed = pd.DataFrame(X_scaled, columns=["N_score", "P_score", "K_score"])
df_processed["crop"] = y

print("Processed P1 dataset:")
print(df_processed.head())

print("\nDataset shape:", df_processed.shape)
