# utils/data_visualization.py

import matplotlib.pyplot as plt
import pandas as pd

class DataVisualization:
    @staticmethod
    def plot_vital_signs(data: pd.DataFrame):
        """Plot vital signs over time."""
        plt.figure(figsize=(12, 6))
        
        # Plot heart rate
        plt.subplot(3, 1, 1)
        plt.plot(data['timestamp'], data['heart_rate'], label='Heart Rate', color='blue')
        plt.title('Heart Rate Over Time')
        plt.xlabel('Time')
        plt.ylabel('Heart Rate (bpm)')
        plt.xticks(rotation=45)
        plt.legend()

        # Plot blood pressure
        plt.subplot(3, 1, 2)
        plt.plot(data['timestamp'], [bp[0] for bp in data['blood_pressure']], label='Systolic', color='red')
        plt.plot(data['timestamp'], [bp[1] for bp in data['blood_pressure']], label='Diastolic', color='orange')
        plt.title('Blood Pressure Over Time')
        plt.xlabel('Time')
        plt.ylabel('Blood Pressure (mmHg)')
        plt.xticks(rotation=45)
        plt.legend()

        # Plot temperature
        plt.subplot(3, 1, 3)
        plt.plot(data['timestamp'], data['temperature'], label='Temperature', color='green')
        plt.title('Body Temperature Over Time')
        plt.xlabel('Time')
        plt.ylabel('Temperature (°F)')
        plt.xticks(rotation=45)
        plt.legend()

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_anomalies(data: pd.DataFrame):
        """Highlight anomalies in vital signs."""
        plt.figure(figsize=(12, 6))
        
        # Plot heart rate with anomalies
        plt.plot(data['timestamp'], data['heart_rate'], label='Heart Rate', color='blue')
        anomalies = data[data['anomaly'] == -1]
        plt.scatter(anomalies['timestamp'], anomalies['heart_rate'], color='red', label='Anomalies', marker='x')
        
        plt.title('Heart Rate with Anomalies Highlighted')
        plt.xlabel('Time')
        plt.ylabel('Heart Rate (bpm)')
        plt.xticks(rotation=45)
        plt.legend()
        plt.show()

# Example usage:
if __name__ == "__main__":
    # Sample data for visualization
    sample_data = pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=10, freq='H'),
        'heart_rate': [70, 72, 75, 80, 150, 78, 76, 74, 73, 71],
        'blood_pressure': [(120, 80)] * 10,
        'temperature': [98.6] * 10,
        'anomaly': [1, 1, 1, 1, -1, 1, 1, 1, 1, 1]
    })
    
    DataVisualization.plot_vital_signs(sample_data)
    DataVisualization.plot_anomalies(sample_data)
