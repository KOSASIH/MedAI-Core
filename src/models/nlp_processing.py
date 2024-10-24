# models/nlp_processing.py

import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from transformers import pipeline

class NLPProcessingModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.sentiment_model = pipeline("sentiment-analysis")
        self.ner_model = pipeline("ner", aggregation_strategy="simple")

    def preprocess_text(self, text: str) -> str:
        """Basic text preprocessing: lowercasing and removing special characters."""
        text = text.lower()
        text = ''.join(char for char in text if char.isalnum() or char.isspace())
        return text

    def vectorize_text(self, texts: list) -> np.ndarray:
        """Convert a list of texts into TF-IDF feature vectors."""
        processed_texts = [self.preprocess_text(text) for text in texts]
        return self.vectorizer.fit_transform(processed_texts).toarray()

    def analyze_sentiment(self, text: str) -> dict:
        """Analyze the sentiment of the given text."""
        processed_text = self.preprocess_text(text)
        return self.sentiment_model(processed_text)[0]

    def extract_entities(self, text: str) -> list:
        """Extract named entities from the given text."""
        processed_text = self.preprocess_text(text)
        return self.ner_model(processed_text)

    def save_vectorizer(self, filename: str):
        """Save the TF-IDF vectorizer to a file."""
        joblib.dump(self.vectorizer, filename)

    def load_vectorizer(self, filename: str):
        """Load the TF-IDF vectorizer from a file."""
        self.vectorizer = joblib.load(filename)

# Example usage:
if __name__ == "__main__":
    nlp_model = NLPProcessingModel()

    # Example texts
    texts = ["I love the new features of MedAI!", "The service was terrible and disappointing."]
    
    # Vectorize texts
    vectors = nlp_model.vectorize_text(texts)
    print("TF-IDF Vectors:\n", vectors)

    # Sentiment analysis
    sentiment = nlp_model.analyze_sentiment("I am very happy with the results!")
    print("Sentiment Analysis:\n", sentiment)

    # Named entity recognition
    entities = nlp_model.extract_entities("Dr. Smith is a renowned cardiologist.")
    print("Named Entities:\n", entities)

    # Save and load the vectorizer
    nlp_model.save_vectorizer("tfidf_vectorizer.joblib")
    loaded_vectorizer = NLPProcessingModel()
    loaded_vectorizer.load_vectorizer("tfidf_vectorizer.joblib")
