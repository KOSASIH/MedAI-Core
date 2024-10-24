# models/anomaly_detection.py

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class AnomalyDetectionModel:
    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.trained = False

    def train(self, data: pd.DataFrame):
        """Train the Isolation Forest model on the provided data."""
        self.model.fit(data)
        self.trained = True

    def predict(self, input_data: pd.DataFrame):
        """Predict anomalies in the input data."""
        if not self.trained:
            raise Exception("Model must be trained before predictions can be made.")
        return self.model.predict(input_data)

    def evaluate(self, input_data: pd.DataFrame, true_labels: np.ndarray):
        """Evaluate the model's performance using classification report."""
        predictions = self.predict(input_data)
        # Convert predictions to binary (1 for normal, -1 for anomaly)
        predictions_binary = np.where(predictions == -1, 1, 0)
        print(classification_report(true_labels, predictions_binary))

    def visualize_anomalies(self, data: pd.DataFrame, predictions: np.ndarray):
        """Visualize the anomalies in the dataset."""
        data['anomaly'] = predictions
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=data, x=data.columns[0], y=data.columns[1], hue='anomaly', palette={0: 'blue', 1: 'red'})
        plt.title('Anomaly Detection Visualization')
        plt.xlabel(data.columns[0])
        plt.ylabel(data.columns[1])
        plt.legend(title='Anomaly', loc='upper right', labels=['Normal', 'Anomaly'])
        plt.show()

    def save_model(self, filename: str):
        """Save the trained model to a file."""
        joblib.dump(self.model, filename)

    def load_model(self, filename: str):
        """Load a trained model from a file."""
        self.model = joblib.load(filename)
        self.trained = True

# Example usage:
anomaly_model = AnomalyDetectionModel(contamination=0.1)
data = pd.read_csv("health_data.csv")  # Assuming health_data.csv contains relevant features
anomaly_model.train(data)

# Predict anomalies
predictions = anomaly_model.predict(data)

# Evaluate the model (assuming true_labels is available)
# true_labels = np.array([...])  # Replace with actual labels
# anomaly_model.evaluate(data, true_labels)

# Visualize anomalies
anomaly_model.visualize_anomalies(data, predictions)

# Save and load the model
anomaly_model.save_model("anomaly_detection_model.joblib")
loaded_model = AnomalyDetectionModel()
loaded_model.load_model("anomaly_detection_model.joblib")
