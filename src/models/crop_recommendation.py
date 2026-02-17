import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


class CropRecommendationModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

    def train(self, df: pd.DataFrame, target_column: str):
        """
        Trains the crop recommendation model.
        """
        X = df.drop(columns=[target_column])
        y = df[target_column]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

        return accuracy

    def predict(self, input_data: pd.DataFrame):
        """
        Predicts crop based on input features.
        """
        return self.model.predict(input_data)
    
    def predict_from_twin(self, twin_state):
        """
        Predict crop directly from a Digital Twin state.
        """
        import pandas as pd

        input_df = pd.DataFrame([twin_state.as_dict()])
        return self.model.predict(input_df)



if __name__ == "__main__":
    print("Crop Recommendation Model module ready")
