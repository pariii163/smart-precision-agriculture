class RecommendationEngine:
    def __init__(self, crop_model, disease_model, class_names):
        self.crop_model = crop_model
        self.disease_model = disease_model
        self.class_names = class_names

    def generate_recommendation(self, twin_state, image):
        """
        Generates a combined recommendation using:
        - Digital Twin (soil-based crop suitability)
        - Image-based disease detection
        """

        # Crop recommendation from soil
        crop_prediction = self.crop_model.predict_from_twin(twin_state)[0]

        # Disease prediction from image
        disease_probs = self.disease_model.predict(image)[0]
        disease_index = disease_probs.argmax()
        disease_label = self.class_names[disease_index]
        disease_confidence = disease_probs[disease_index]

        # Decision logic (simple & explainable)
        if disease_label != "healthy":
            advice = (
                f"Crop suitable: {crop_prediction}. "
                f"Disease detected ({disease_label}) with confidence "
                f"{disease_confidence:.2f}. Consider treatment."
            )
        else:
            advice = (
                f"Crop suitable: {crop_prediction}. "
                f"Plant appears healthy. Continue monitoring."
            )

        return {
            "recommended_crop": crop_prediction,
            "plant_health": disease_label,
            "confidence": float(disease_confidence),
            "advice": advice
        }
