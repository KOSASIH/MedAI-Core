# services/health_monitoring.py

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime

class HealthMonitoringService:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05)  # 5% contamination for anomaly detection
        self.data = pd.DataFrame(columns=['timestamp', 'heart_rate', 'blood_pressure', 'temperature'])

    def add_vital_signs(self, heart_rate: float, blood_pressure: tuple, temperature: float):
        """Add new vital signs to the monitoring system."""
        timestamp = datetime.now()
        self.data = self.data.append({
            'timestamp': timestamp,
            'heart_rate': heart_rate,
            'blood_pressure': blood_pressure,
            'temperature': temperature
        }, ignore_index=True)

    def detect_anomalies(self):
        """Detect anomalies in the vital signs."""
        if len(self.data) < 2:
            return "Not enough data to detect anomalies."
        
        features = self.data[['heart_rate', 'temperature']]
        self.model.fit(features)
        self.data['anomaly'] = self.model.predict(features)
        
        anomalies = self.data[self.data['anomaly'] == -1]
        return anomalies if not anomalies.empty else "No anomalies detected."

# Example usage:
if __name__ == "__main__":
    health_monitor = HealthMonitoringService()
    health_monitor.add_vital_signs(75, (120, 80), 98.6)
    health_monitor.add_vital_signs(90, (130, 85), 99.1)
    print(health_monitor.detect_anomalies())
