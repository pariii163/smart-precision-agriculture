import pandas as pd
import joblib
from region_map import STATE_TO_ZONE

# Load trained region-aware model and encoder
model = joblib.load("src/models/crop_recommendation_rf_region.pkl")
encoder = joblib.load("src/models/zone_encoder.pkl")

# Load SHC soil features
shc_path = "data/soil_datasets/shc_soil_features.csv"
df_shc = pd.read_csv(shc_path)

# Prepare soil features
X_soil = df_shc[["N_score", "P_score", "K_score"]].copy()
X_soil["OC_score"] = X_soil.mean(axis=1)

# Map State/UT to agro-climatic zone
df_shc["zone"] = df_shc["State/UT"].apply(
    lambda x: STATE_TO_ZONE.get(x, STATE_TO_ZONE["DEFAULT"])
)

# Encode zone
zone_encoded = encoder.transform(df_shc[["zone"]])
zone_cols = encoder.get_feature_names_out(["zone"])
df_zone = pd.DataFrame(zone_encoded, columns=zone_cols)

# Final feature matrix
X_final = pd.concat([X_soil.reset_index(drop=True), df_zone], axis=1)

# Predict crops
predicted_crops = model.predict(X_final)

# Attach predictions
df_results = df_shc.copy()
df_results["recommended_crop"] = predicted_crops

print("\nRegion-aware crop recommendations based on SHC data:\n")
print(df_results[["State/UT", "zone", "recommended_crop"]])
