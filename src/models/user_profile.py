# models/user_profile.py

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

class UserProfileModel:
    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=self.n_clusters)
        self.scaler = StandardScaler()
        self.pipeline = None

    def create_pipeline(self):
        """Create a preprocessing and clustering pipeline."""
        numeric_features = ['age', 'income', 'health_score']  # Example numeric features
        categorical_features = ['gender', 'smoking_status']  # Example categorical features

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        self.pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                         ('clusterer', self.model)])

    def preprocess_data(self, data: pd.DataFrame):
        """Preprocess the data by scaling features and handling missing values."""
        if self.pipeline is None:
            self.create_pipeline()
        return self.pipeline.named_steps['preprocessor'].fit_transform(data)

    def fit(self, data: pd.DataFrame):
        """Fit the KMeans model to the user data."""
        data_processed = self.preprocess_data(data)
        self.model.fit(data_processed)

    def predict(self, input_data: pd.DataFrame):
        """Predict user clusters based on input data."""
        input_data_processed = self.pipeline.named_steps['preprocessor'].transform(input_data)
        return self.model.predict(input_data_processed)

    def get_cluster_centers(self):
        """Get the centers of the clusters."""
        return self.model.cluster_centers_

    def save_model(self, filename: str):
        """Save the trained model to a file."""
        joblib.dump(self.pipeline, filename)

    def load_model(self, filename: str):
        """Load a trained model from a file."""
        self.pipeline = joblib.load(filename)

    def enrich_user_profiles(self, external_data: pd.DataFrame):
        """Enrich user profiles with external data sources."""
        # Example: Merge with external data to enhance user profiles
        # This could include demographic data, health records, etc.
        enriched_data = pd.merge(self.data, external_data, on='user_id', how='left')
        return enriched_data

    def dynamic_clustering(self, new_data: pd.DataFrame):
        """Update clusters dynamically with new user data."""
        print("Updating clusters with new user data...")
        self.fit(new_data)
        print("Clusters updated successfully!")

# Example usage:
user_model = UserProfileModel(n_clusters=5)
data = pd.read_csv("user_data.csv")
user_model.fit(data)

# Predict user clusters
input_data = pd.DataFrame({'age': [25, 35, 45], 'income': [50000, 60000, 70000], 'health_score': [80, 90, 70]})
predictions = user_model.predict(input_data)
print(predictions)

# Enrich user profiles with external data
external_data = pd.read_csv("external_data.csv")
enriched_profiles = user_model.enrich_user_profiles(external_data)
print(enriched_profiles)

# Save and load the model
user_model.save_model("user_profile_model.joblib")
loaded_model = UserProfileModel()
loaded_model.load_model("user_profile_model.joblib")
