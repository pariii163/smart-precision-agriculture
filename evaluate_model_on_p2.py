import pandas as pd
import joblib
from region_map import STATE_TO_ZONE

# Load trained region-aware model and encoder
model = joblib.load("src/models/crop_recommendation_rf_region.pkl")
encoder = joblib.load("src/models/zone_encoder.pkl")

# Load P2 dataset
df = pd.read_csv("data/soil_datasets/crop_geo.csv")

# ---- Convert categorical soil presence to scores ----
def presence_score(row, high, medium, low):
    if str(row[high]).strip() != "":
        return 3
    elif str(row[medium]).strip() != "":
        return 2
    elif str(row[low]).strip() != "":
        return 1
    else:
        return 0

df_features = pd.DataFrame()

df_features["N_score"] = df.apply(
    lambda x: presence_score(
        x, "Nitrogen - High", "Nitrogen - Medium", "Nitrogen - Low"
    ),
    axis=1
)

df_features["P_score"] = df.apply(
    lambda x: presence_score(
        x, "Phosphorous - High", "Phosphorous - Medium", "Phosphorous - Low"
    ),
    axis=1
)

df_features["K_score"] = df.apply(
    lambda x: presence_score(
        x, "Potassium - High", "Potassium - Medium", "Potassium - Low"
    ),
    axis=1
)

# Approximate OC as mean nutrient richness
df_features["OC_score"] = df_features[["N_score", "P_score", "K_score"]].mean(axis=1)

# ---- Region handling ----
df_features["zone"] = df["Region"].apply(
    lambda x: STATE_TO_ZONE.get(x, STATE_TO_ZONE["DEFAULT"])
)

# Encode zone
zone_encoded = encoder.transform(df_features[["zone"]])
zone_cols = encoder.get_feature_names_out(["zone"])
df_zone = pd.DataFrame(zone_encoded, columns=zone_cols)

# Final feature matrix
X_final = pd.concat(
    [df_features.drop(columns=["zone"]), df_zone],
    axis=1
)

# Target
y_true = df["Crop"]

# Predict
y_pred = model.predict(X_final)

# Evaluate robustness
from sklearn.metrics import accuracy_score, classification_report

print("Robustness Evaluation on P2 (Geo-Referenced Soil Dataset)")
print("-------------------------------------------------------")
print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_true, y_pred))
