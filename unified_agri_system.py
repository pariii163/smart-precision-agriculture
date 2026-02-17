import numpy as np
import joblib
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from region_map import STATE_TO_ZONE
from sklearn.preprocessing import MinMaxScaler

# -----------------------------
# Load Models
# -----------------------------
crop_model = joblib.load("src/models/crop_recommendation_rf_region.pkl")
zone_encoder = joblib.load("src/models/zone_encoder.pkl")
crop_scaler = joblib.load("src/models/crop_scaler.pkl")


disease_model = tf.keras.models.load_model(
    "src/models/plant_disease_cnn_baseline.h5"
)

# -----------------------------------
# Regional Crop Suitability Weights
# -----------------------------------

REGION_CROP_WEIGHTS = {
    "Tropical": {
        "coconut": 1.3,
        "banana": 1.2,
        "rice": 1.15,
        "coffee": 1.1
    },
    "Subtropical": {
        "wheat": 1.2,
        "maize": 1.15,
        "mustard": 1.1
    },
    "Semi-Arid": {
        "cotton": 1.25,
        "millet": 1.3,
        "jute": 0.9
    },
    "Arid": {
        "millet": 1.35,
        "cotton": 1.2,
        "rice": 0.8
    },
    "Temperate": {
        "apple": 1.4,
        "grapes": 1.2,
        "maize": 1.1
    }
}


# -----------------------------
# Crop Recommendation Function
# -----------------------------
def recommend_crop(N, P, K, state):

    # Normalize NPK using saved scaler
    X = crop_scaler.transform([[N, P, K]])
    N_score, P_score, K_score = X[0]

    OC_score = np.mean([N_score, P_score, K_score])

    # Region encoding
    zone = STATE_TO_ZONE.get(state, STATE_TO_ZONE["DEFAULT"])
    zone_encoded = zone_encoder.transform([[zone]])

    # Final feature vector
    X_final = np.concatenate(
        [[N_score, P_score, K_score, OC_score], zone_encoded[0]]
    ).reshape(1, -1)

    # Get model probabilities
    probs = crop_model.predict_proba(X_final)[0]
    classes = crop_model.classes_

    # Pair crops with probabilities
    all_predictions = list(zip(classes, probs))

    # Sort full model output
    sorted_model = sorted(
        all_predictions,
        key=lambda x: x[1],
        reverse=True
    )

    # Take Top 5 shortlist from model
    top_5 = sorted_model[:5]

    # Get region suitability weights
    zone_weights = REGION_CROP_WEIGHTS.get(zone, {})

    # Apply conditional boosting ONLY within top 5
    adjusted_top_5 = []

    for crop_name, prob in top_5:
        weight = zone_weights.get(crop_name, 1.0)
        adjusted_prob = prob * weight
        adjusted_top_5.append((crop_name, adjusted_prob))

    # Normalize within top 5
    total = sum(prob for _, prob in adjusted_top_5)
    normalized_top_5 = [
        (crop_name, prob / total)
        for crop_name, prob in adjusted_top_5
    ]

    # Re-sort after regional refinement
    final_sorted = sorted(
        normalized_top_5,
        key=lambda x: x[1],
        reverse=True
    )

    # Take final Top 3
    top_3 = final_sorted[:3]

    top_3_formatted = [
        {"crop": crop, "confidence": round(float(prob), 4)}
        for crop, prob in top_3
    ]

    return top_3_formatted



    # Format nicely
    top_3_formatted = [
        {"crop": crop, "confidence": round(float(prob), 4)}
        for crop, prob in top_3
    ]

    return top_3_formatted



# -----------------------------
# Disease Detection Function
# -----------------------------
def detect_disease(image_path):

    img = image.load_img(image_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = disease_model.predict(img_array)[0][0]

    if prediction > 0.5:
        label = "Healthy"
        confidence = prediction
    else:
        label = "Diseased"
        confidence = 1 - prediction

    return label, float(confidence)

# -----------------------------
# Unified Advisory Function
# -----------------------------
def generate_advice(N, P, K, state, image_path):

    top_crops = recommend_crop(N, P, K, state)

    health_status, confidence = detect_disease(image_path)

    primary_crop = top_crops[0]["crop"]

    if health_status == "Healthy":
        advice = f"Top recommendation: {primary_crop}. Plant appears healthy. Continue monitoring."
    else:
        advice = f"Top recommendation: {primary_crop}. Plant shows signs of disease. Consider treatment."

    return {
       "top_crops": top_crops,
       "plant_health": health_status,
       "confidence": round(confidence, 4),
       "advice": advice
    }



# -----------------------------
# Example Run
# -----------------------------
if __name__ == "__main__":

    # Example soil input
    N = 90
    P = 42
    K = 43
    state = "Maharashtra"

    # Example image
    image_path = "data/image_datasets/test/healthy/ff8b36d5-feaf-4d2d-8126-18670a312657___RS_HL 0229.jpg"

    result = generate_advice(N, P, K, state, image_path)

    print("\nFINAL SYSTEM OUTPUT")
    print("-------------------")
    for key, value in result.items():
        print(f"{key}: {value}")
