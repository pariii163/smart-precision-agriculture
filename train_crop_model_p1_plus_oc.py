import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import MinMaxScaler

# Load P1 dataset
file_path = "data/soil_datasets/crop_recommendation.csv"
df = pd.read_csv(file_path)

# Base features
X = df[["N", "P", "K"]]
y = df["label"]

# ---- OC proxy (important) ----
# Since P1 does not have OC, we approximate OC using NPK richness
# This is explicitly documented as an approximation in research
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

df_features = pd.DataFrame(
    X_scaled, columns=["N_score", "P_score", "K_score"]
)

# Approximate OC as mean nutrient richness
df_features["OC_score"] = df_features.mean(axis=1)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    df_features, y, test_size=0.2, random_state=42, stratify=y
)

# Train extended model
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Extended Crop Model (NPK + OC)")
print("--------------------------------")
print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save extended model
model_path = "src/models/crop_recommendation_rf_plus_oc.pkl"
joblib.dump(model, model_path)

print(f"\nSaved extended model to: {model_path}")
