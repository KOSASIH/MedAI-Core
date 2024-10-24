# models/computer_vision.py

import cv2
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array

class ComputerVisionModel:
    def __init__(self, classification_model_path: str):
        self.classification_model = load_model(classification_model_path)
        self.label_encoder = LabelEncoder()
        self.object_detection_model = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'ssd_mobilenet_v2_coco.pbtxt')

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess the image for classification."""
        image = cv2.resize(image, (224, 224))  # Resize to fit the model input
        image = img_to_array(image)
        image = preprocess_input(image)
        return np.expand_dims(image, axis=0)

    def classify_image(self, image: np.ndarray) -> str:
        """Classify the given image using the pre-trained model."""
        processed_image = self.preprocess_image(image)
        predictions = self.classification_model.predict(processed_image)
        class_index = np.argmax(predictions, axis=1)
        return self.label_encoder.inverse_transform(class_index)[0]

    def detect_objects(self, image: np.ndarray) -> list:
        """Detect objects in the given image using a pre-trained object detection model."""
        blob = cv2.dnn.blobFromImage(image, 0.007843, (300, 300), 127.5)
        self.object_detection_model.setInput(blob)
        detections = self.object_detection_model.forward()
        
        detected_objects = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Confidence threshold
                class_id = int(detections[0, 0, i, 1])
                detected_objects.append((class_id, confidence))
        return detected_objects

    def save_label_encoder(self, filename: str):
        """Save the label encoder to a file."""
        joblib.dump(self.label_encoder, filename)

    def load_label_encoder(self, filename: str):
        """Load the label encoder from a file."""
        self.label_encoder = joblib.load(filename)

# Example usage:
if __name__ == "__main__":
    cv_model = ComputerVisionModel('classification_model.h5')

    # Load an image
    image = cv2.imread('example_image.jpg')

    # Classify the image
    class_label = cv_model.classify_image(image)
    print("Classified Label:\n", class_label)

    # Detect objects in the image
    detected_objects = cv_model.detect_objects(image)
    print("Detected Objects:\n", detected_objects)

    # Save and load the label encoder
    cv_model.save_label_encoder("label_encoder.joblib")
    loaded_encoder = ComputerVisionModel('classification_model.h5')
    loaded_encoder.load_label_encoder("label_encoder.joblib")
