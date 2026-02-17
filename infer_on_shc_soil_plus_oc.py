import pandas as pd
import joblib

# Load extended model
model = joblib.load("src/models/crop_recommendation_rf_plus_oc.pkl")

# Load SHC soil features
shc_path = "data/soil_datasets/shc_soil_features.csv"
df_shc = pd.read_csv(shc_path)

# Prepare features
X_shc = df_shc[["N_score", "P_score", "K_score"]].copy()

# Approximate OC_score consistently (same logic as training)
X_shc["OC_score"] = X_shc.mean(axis=1)

# Rename to match training schema
X_shc.columns = ["N_score", "P_score", "K_score", "OC_score"]

# Predict crops
predicted_crops = model.predict(X_shc)

# Attach results
df_results = df_shc.copy()
df_results["recommended_crop"] = predicted_crops

print("\nCrop recommendations (Extended Model):\n")
print(df_results[["State/UT", "recommended_crop"]])
