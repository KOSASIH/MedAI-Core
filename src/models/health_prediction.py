# models/health_prediction.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import joblib
from sklearn.preprocessing import StandardScaler
import shap  # SHAP for explainability
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

class HealthPredictionModel:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.trained = False
        self.scaler = StandardScaler()
        self.pipeline = None

    def create_pipeline(self):
        """Create a preprocessing and modeling pipeline."""
        numeric_features = ['age', 'blood_pressure', 'cholesterol']  # Example numeric features
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
                                         ('classifier', self.model)])

    def preprocess_data(self, data: pd.DataFrame):
        """Preprocess the data by scaling features and handling missing values."""
        if self.pipeline is None:
            self.create_pipeline()
        return self.pipeline.named_steps['preprocessor'].fit_transform(data)

    def train(self, data: pd.DataFrame, target_column: str):
        """Train the model using the provided data."""
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X_processed = self.preprocess_data(X)
        X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)
        self.pipeline.fit(X_train, y_train)
        self.trained = True
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(classification_report(y_test, y_pred))
        return accuracy

    def tune_hyperparameters(self, data: pd.DataFrame, target_column: str):
        """Tune hyperparameters using GridSearchCV."""
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X_processed = self.preprocess_data(X)
        param_grid = {
            'classifier__n_estimators': [50, 100, 200],
            'classifier__max_depth': [None, 10, 20, 30],
            'classifier__min_samples_split': [2, 5, 10]
        }
        grid_search = GridSearchCV(self.pipeline, param_grid, cv=3, scoring='accuracy')
        grid_search.fit(X_processed, y)
        self.pipeline = grid_search.best_estimator_
        print(f"Best parameters: {grid_search.best_params_}")

    def explain_predictions(self, input_data: pd.DataFrame):
        """Explain model predictions using SHAP."""
        if not self.trained:
            raise Exception("Model must be trained before predictions can be explained.")
        input_data_processed = self.pipeline.named_steps['preprocessor'].transform(input_data)
        explainer = shap.TreeExplainer(self.pipeline.named_steps['classifier'])
        shap_values = explainer.shap_values(input_data_processed)
        return shap_values

    def predict(self, input_data: pd.DataFrame):
        """Make predictions using the trained model."""
        if not self.trained:
            raise Exception("Model must be trained before predictions can be made.")
        input_data_processed = self.pipeline.named_steps['preprocessor'].transform(input_data)
        return self.pipeline.predict(input_data_processed)

    def save_model(self, filename: str):
        """Save the trained model to a file."""
        joblib.dump(self.pipeline, filename)

    def load_model(self, filename: str):
        """Load a trained model from a file."""
        self.pipeline = joblib.load(filename)
        self.trained = True

    def automated_retraining(self, new_data: pd.DataFrame, target_column: str):
        """Automate model retraining with new data."""
        print("Retraining model with new data...")
 self.train(new_data, target_column)
        print("Model retrained successfully!")

# Example usage:
health_model = HealthPredictionModel()
data = pd.read_csv("health_data.csv")
health_model.train(data, "health_outcome")
health_model.tune_hyperparameters(data, "health_outcome")
health_model.save_model("health_prediction_model.joblib")

# Load the model and make predictions
loaded_model = HealthPredictionModel()
loaded_model.load_model("health_prediction_model.joblib")
input_data = pd.DataFrame({'age': [30, 40, 50], 'blood_pressure': [120, 130, 140], 'cholesterol': [200, 220, 240]})
predictions = loaded_model.predict(input_data)
print(predictions)

# Explain predictions
shap_values = loaded_model.explain_predictions(input_data)
print(shap_values)
