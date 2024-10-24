# src/main/config.py

import os

class Config:
    """Configuration settings for the MedAI-Core application."""
    
    DEBUG = os.getenv('DEBUG', 'True') == ' True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///medai_core.db')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key_here')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://guest:guest@localhost//')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'rpc://')

    @staticmethod
    def init_app(app):
        """Initialize the application with the given configuration."""
        pass
