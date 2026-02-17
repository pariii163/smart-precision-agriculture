import cv2
import numpy as np
from pathlib import Path


class DiseaseDetectionModel:
    def __init__(self, image_size=(224, 224)):
        self.image_size = image_size
        self.model = None  # CNN will be added later

    def load_image(self, image_path: str) -> np.ndarray:
        """
        Loads and preprocesses a single image.
        """
        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError("Failed to load image")

        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize image
        image = cv2.resize(image, self.image_size)

        # Normalize pixel values
        image = image / 255.0

        return image

    def load_images_from_folder(self, folder_path: str):
        """
        Loads all images from a folder.
        """
        folder = Path(folder_path)

        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        images = []

        for img_path in folder.iterdir():
            if img_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                img = self.load_image(img_path)
                images.append(img)

        return np.array(images)
    
    def load_labeled_images(self, base_folder: str):
        """
        Loads images and labels from a directory structure:
        base_folder/
            healthy/
            diseased/
        """
        base_folder = Path(base_folder)

        if not base_folder.exists():
            raise FileNotFoundError(f"Base folder not found: {base_folder}")

        images = []
        labels = []

        class_names = sorted([d.name for d in base_folder.iterdir() if d.is_dir()])

        for label_index, class_name in enumerate(class_names):
            class_folder = base_folder / class_name

            for img_path in class_folder.iterdir():
                if img_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                    img = self.load_image(img_path)
                    images.append(img)
                    labels.append(label_index)

        return np.array(images), np.array(labels), class_names
    
    
    def build_cnn(self, num_classes: int):
        """
        Builds a simple CNN model.
        """
        import tensorflow as tf

        Sequential = tf.keras.models.Sequential
        Conv2D = tf.keras.layers.Conv2D
        MaxPooling2D = tf.keras.layers.MaxPooling2D
        Flatten = tf.keras.layers.Flatten
        Dense = tf.keras.layers.Dense
        Dropout = tf.keras.layers.Dropout


        model = Sequential([
            Conv2D(32, (3, 3), activation="relu", input_shape=(224, 224, 3)),
            MaxPooling2D(2, 2),

            Conv2D(64, (3, 3), activation="relu"),
            MaxPooling2D(2, 2),

            Flatten(),
            Dense(128, activation="relu"),
            Dropout(0.5),
            Dense(num_classes, activation="softmax")
        ])

        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"]
        )

        self.model = model
        return model


    def train(self, X_train, y_train, epochs=5, batch_size=8):
        """
        Trains the CNN model.
        """
        if self.model is None:
            raise ValueError("Model is not built yet")

        history = self.model.fit(
            X_train,
            y_train,
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )

        return history


    def predict(self, image: np.ndarray):
        """
        Predicts disease class for a single image.
        """
        if self.model is None:
            raise ValueError("Model is not trained yet")

        image = np.expand_dims(image, axis=0)
        prediction = self.model.predict(image)

        return prediction




if __name__ == "__main__":
    print("Disease detection image loader ready")
