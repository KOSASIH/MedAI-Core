# tests/test_health_prediction.py

import unittest
import pandas as pd
from services.health_monitoring import HealthMonitoringService

class TestHealthMonitoringService(unittest.TestCase):
    def setUp(self):
        self.service = HealthMonitoringService()

    def test_add_vital_signs(self):
        self.service.add_vital_signs(75, (120, 80), 98.6)
        self.assertEqual(len(self.service.data), 1)

    def test_detect_anomalies_no_data(self):
        result = self.service.detect_anomalies()
        self.assertEqual(result, "Not enough data to detect anomalies.")

    def test_detect_anomalies(self):
        # Adding normal vital signs
        self.service.add_vital_signs(75, (120, 80), 98.6)
        self.service.add_vital_signs(90, (130, 85), 99.1)
        # Adding an anomalous vital sign
        self.service.add_vital_signs(150, (180, 120), 101.0)
        
        anomalies = self.service.detect_anomalies()
        self.assertTrue(isinstance(anomalies, pd.DataFrame))
        self.assertGreater(len(anomalies), 0)

if __name__ == '__main__':
    unittest.main()
