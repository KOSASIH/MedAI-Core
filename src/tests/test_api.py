# tests/test_api.py

import unittest
import json
from api.routes import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_vital_signs(self):
        response = self.app.post('/api/v1/health_monitoring', 
                                  data=json.dumps({
                                      "heart_rate": 75,
                                      "blood_pressure": (120, 80),
                                      "temperature": 98.6
                                  }), 
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("Vital signs added successfully.", response.get_data(as_text=True))

    def test_detect_anomalies(self):
        # First, add some vital signs
        self.app.post('/api/v1/health_monitoring', 
                      data=json.dumps({
                          "heart_rate": 75,
                          "blood_pressure": (120, 80),
                          "temperature": 98.6
                      }), 
                      content_type='application/json')
        self.app.post('/api/v1/health_monitoring', 
                      data=json.dumps({
                          "heart_rate": 150,
                          "blood_pressure": (180, 120),
                          "temperature": 101.0
                      }), 
                      content_type='application/json')
        
        response = self.app.get('/api/v1/health_monitoring/anomalies')
        self.assertEqual(response.status_code, 200)
        self.assertIn("anomaly", response.get_data(as_text=True))

    def test_ask_question(self):
        response = self.app.post('/api/v1/virtual_assistant', 
                                  data=json.dumps({
                                      "question": "What is a balanced diet?",
                                      "context": "A balanced diet includes a variety of foods from all food groups."
                                  }), 
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("balanced diet", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
