import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load P1 dataset
file_path = "data/soil_datasets/crop_recommendation.csv"
df = pd.read_csv(file_path)

# Features and target
X = df[["N", "P", "K"]]
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Baseline Crop Recommendation Model")
print("----------------------------------")
print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model to src/models/
model_path = "src/models/crop_recommendation_rf_baseline.pkl"
joblib.dump(model, model_path)

print(f"\nSaved trained model to: {model_path}")
