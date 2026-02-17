import joblib

model = joblib.load("src/models/crop_recommendation_rf_region.pkl")

print("Feature count expected by model:", model.n_features_in_)
print("Classes:", model.classes_)
