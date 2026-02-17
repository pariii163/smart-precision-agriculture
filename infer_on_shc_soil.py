import pandas as pd
import joblib

# Load trained model
model = joblib.load("src/models/crop_recommendation_rf_baseline.pkl")

# Load processed SHC soil features
shc_path = "data/soil_datasets/shc_soil_features.csv"
df_shc = pd.read_csv(shc_path)

# Rename SHC features to match training schema
X_shc = df_shc[["N_score", "P_score", "K_score"]].copy()
X_shc.columns = ["N", "P", "K"]

# Predict recommended crops
predicted_crops = model.predict(X_shc)

# Attach predictions
df_results = df_shc.copy()
df_results["recommended_crop"] = predicted_crops

print("\nCrop recommendations based on SHC soil data:\n")
print(df_results[["State/UT", "recommended_crop"]])
