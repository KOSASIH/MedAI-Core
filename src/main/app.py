# src/main/app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_restplus import Api, Resource
from marshmallow import ValidationError
from config import Config
from logger import setup_logging
from models import db, User, HealthData
from schemas import UserSchema, HealthDataSchema
from tasks import send_welcome_email
import logging

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

# Initialize JWT
jwt = JWTManager(app)

# Initialize API
api = Api(app, version='1.0', title='MedAI-Core API', description='API for MedAI-Core Health Management System')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to MedAI-Core API!"})

@api.route('/users/register')
class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        user_schema = UserSchema()
        try:
            user = user_schema.load(data)
            db.session.add(user)
            db.session.commit()
            logger.info(f"User  registered: {user.username}")
            send_welcome_email.delay(user.email)  # Asynchronous task
            return jsonify({"message": "User  registered successfully!"}), 201
        except ValidationError as err:
            return jsonify(err.messages), 400

@api.route('/users/login')
class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and user.verify_password(data['password']):
            access_token = create_access_token(identity=user.id)
            logger.info(f"User  logged in: {user.username}")
            return jsonify(access_token=access_token), 200
        return jsonify({"message": "Invalid credentials"}), 401

@api.route('/users/<int:user_id>/health-data')
class HealthDataResource(Resource):
    @jwt_required()
    def post(self, user_id):
        current_user = get_jwt_identity()
        if current_user != user_id:
            return jsonify({"message": "Unauthorized"}), 403

        data = request.get_json()
        health_data_schema = HealthDataSchema()
        try:
            health_data = health_data_schema.load(data)
            health_data.user_id = user_id
            db.session.add(health_data)
            db.session.commit()
            logger.info(f"Health data submitted for user {user_id}: {data}")
            return jsonify({"message": "Health data submitted successfully!"}), 200
        except ValidationError as err:
            return jsonify(err.messages), 400

@api.route('/assistant/chat')
class ChatAssistant(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        logger.info(f"User  message to assistant: {data['message']}")
        response = {"response": "This is a response from the virtual assistant."}
        return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
