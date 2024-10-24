# services/data_processing.py

import pandas as pd
from sklearn.preprocessing import StandardScaler

class DataProcessing:
    def __init__(self):
        self.scaler = StandardScaler()

    def normalize_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Normalize the data using StandardScaler."""
        numeric_cols = data.select_dtypes(include=['float64', 'int']).columns
        data[numeric_cols] = self.scaler.fit_transform(data[numeric_cols])
        return data

    def extract_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Extract relevant features from the dataset."""
        # Example feature extraction: calculating BMI from weight and height
        if 'weight' in data.columns and 'height' in data.columns:
            data['BMI'] = data['weight'] / (data['height'] ** 2)
        return data

# Example usage:
if __name__ == "__main__":
    dp = DataProcessing()
    sample_data = pd.DataFrame({
        'weight': [70, 80, 60],
        'height': [1.75, 1.80, 1.65]
    })
    normalized_data = dp.normalize_data(sample_data)
    feature_data = dp.extract_features(normalized_data)
    print("Normalized Data:\n", normalized_data)
    print("Feature Data:\n", feature_data)
