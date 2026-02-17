import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from region_map import STATE_TO_ZONE

# Load P1 dataset
df = pd.read_csv("data/soil_datasets/crop_recommendation.csv")

# Base soil features
X_base = df[["N", "P", "K"]]
y = df["label"]

# Normalize NPK
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_base)
df_features = pd.DataFrame(X_scaled, columns=["N_score", "P_score", "K_score"])

# Approximate OC
df_features["OC_score"] = df_features.mean(axis=1)

# Add REGION (synthetic, for training robustness)
# Since P1 doesn't have state, we simulate zone exposure
import numpy as np
zones = ["Tropical", "Subtropical", "Semi-Arid", "Arid", "Temperate"]
df_features["zone"] = np.random.choice(zones, size=len(df_features))

# One-hot encode region
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
zone_encoded = encoder.fit_transform(df_features[["zone"]])
zone_cols = encoder.get_feature_names_out(["zone"])
df_zone = pd.DataFrame(zone_encoded, columns=zone_cols)

# Final feature set
X_final = pd.concat(
    [df_features.drop(columns=["zone"]), df_zone],
    axis=1
)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_final, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(n_estimators=400, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Region-aware Crop Model")
print("------------------------")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model and encoder
joblib.dump(model, "src/models/crop_recommendation_rf_region.pkl")
joblib.dump(encoder, "src/models/zone_encoder.pkl")
joblib.dump(scaler, "src/models/crop_scaler.pkl")


print("\nSaved region-aware model and encoder.")
