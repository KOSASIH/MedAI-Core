# api/routes.py

from flask import Flask, request, jsonify
from services.health_monitoring import HealthMonitoringService
from services.virtual_assistant import VirtualHealthAssistant
from services.data_processing import DataProcessing

app = Flask(__name__)

# Initialize services
health_monitor = HealthMonitoringService()
assistant = VirtualHealthAssistant()
data_processor = DataProcessing()

@app.route('/api/v1/health_monitoring', methods=['POST'])
def add_vital_signs():
    """Endpoint to add vital signs for health monitoring."""
    data = request.json
    heart_rate = data.get('heart_rate')
    blood_pressure = data.get('blood_pressure')
    temperature = data.get('temperature')
    
    health_monitor.add_vital_signs(heart_rate, blood_pressure, temperature)
    return jsonify({"message": "Vital signs added successfully."}), 201

@app.route('/api/v1/health_monitoring/anomalies', methods=['GET'])
def detect_anomalies():
    """Endpoint to detect anomalies in vital signs."""
    anomalies = health_monitor.detect_anomalies()
    return jsonify(anomalies), 200

@app.route('/api/v1/virtual_assistant', methods=['POST'])
def ask_question():
    """Endpoint for the virtual health assistant to answer questions."""
    data = request.json
    question = data.get('question')
    context = data.get('context')
    
    answer = assistant.answer_question(question, context)
    return jsonify({"answer": answer}), 200

@app.route('/api/v1/health_tips', methods=['GET'])
def get_health_tip():
    """Endpoint to get health tips."""
    category = request.args.get('category')
    tip = assistant.get_health_tip(category)
    return jsonify({"tip": tip}), 200

@app.route('/api/v1/data_processing/normalize', methods=['POST'])
def normalize_data():
    """Endpoint to normalize data."""
    data = request.json
    df = data_processor.normalize_data(pd.DataFrame(data))
    return jsonify(df.to_dict(orient='records')), 200

@app.route('/api/v1/data_processing/extract_features', methods=['POST'])
def extract_features():
    """Endpoint to extract features from data."""
    data = request.json
    df = data_processor.extract_features(pd.DataFrame(data))
    return jsonify(df.to_dict(orient='records')), 200

if __name__ == "__main__":
    app.run(debug=True)
