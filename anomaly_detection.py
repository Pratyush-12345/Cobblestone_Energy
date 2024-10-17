import numpy as np
import time
import random
from collections import deque
import plotly.graph_objects as go
import asyncio

# --- Custom Exception for Data Stream ---
class DataStreamException(Exception):
    """Custom exception to handle invalid data in the stream."""
    pass

# --- Data Validation ---
def validate_data(value):
    """Validate incoming data to ensure it is a floating-point number."""
    if not isinstance(value, (int, float)):
        raise DataStreamException(f"Invalid data: {value}")
    return True

# --- Data Stream Simulation ---
def data_stream_simulation():
    """
    Simulates a real-time data stream with seasonality, noise, and random anomalies.
    
    The stream generates a floating-point number with a regular sinusoidal pattern (seasonality), 
    random noise, and occasional random anomalies to mimic real-world scenarios.
    """
    t = 0
    while True:
        try:
            # Generate sinusoidal seasonal pattern with added random noise
            seasonality = 10 * np.sin(2 * np.pi * t / 50)
            noise = np.random.normal(0, 2)
            value = 50 + seasonality + noise

            # Randomly inject anomalies (5% chance)
            if random.random() < 0.05:
                value += np.random.normal(30, 10)  # Inject anomaly

            # Validate data to ensure correctness
            validate_data(value)

            t += 1
            yield value
            time.sleep(0.1)  # Simulate real-time delay
        except DataStreamException as e:
            print(f"Error in data stream: {e}")
            continue

# --- Exponential Moving Average (EMA) Anomaly Detector ---
class EMAAnomalyDetector:
    """
    Anomaly detection using an Exponential Moving Average (EMA) approach.

    The algorithm calculates the EMA and standard deviation to detect anomalies 
    based on Z-score. An anomaly is flagged when the absolute Z-score exceeds 
    the predefined threshold.
    
    - `alpha`: Smoothing factor for EMA.
    - `threshold`: Z-score threshold for anomaly detection.
    """
    def __init__(self, alpha=0.1, threshold=3):
        self.ema = None  # Exponential Moving Average (initially None)
        self.alpha = alpha  # Smoothing factor for EMA
        self.std = None  # Standard deviation (initially None)
        self.threshold = threshold  # Z-score threshold for anomaly detection

    def update_ema(self, value):
        """Update EMA with new value and return True if an anomaly is detected."""
        try:
            # Initialize EMA and std on first value
            if self.ema is None:
                self.ema = value
                self.std = 0
            else:
                # Update EMA using the exponential smoothing formula
                self.ema = self.alpha * value + (1 - self.alpha) * self.ema
                # Update standard deviation
                self.std = np.sqrt(self.alpha * (value - self.ema) ** 2 + (1 - self.alpha) * self.std ** 2)

            # Compute Z-score
            z_score = (value - self.ema) / (self.std if self.std > 0 else 1)
            # Return True if the Z-score exceeds the anomaly threshold
            return abs(z_score) > self.threshold
        except ZeroDivisionError:
            print(f"Warning: Standard deviation is zero, cannot compute Z-score.")
            return False
        except Exception as e:
            print(f"Error in EMA calculation: {e}")
            return False

# --- Real-time Plotly Visualization ---
async def live_visualization():
    """
    Real-time visualization of the data stream and detected anomalies.

    - The data stream is plotted as a line.
    - Anomalies are marked as red dots.
    """
    fig = go.FigureWidget()
    fig.add_scatter(name="Data Stream", mode="lines")
    fig.add_scatter(name="Anomalies", mode="markers", marker=dict(color='red', size=10))
    display(fig)

    data_x = deque(maxlen=200)  # Store recent 200 data points
    data_y = deque(maxlen=200)
    anomaly_x = []  # Store anomaly x-coordinates
    anomaly_y = []  # Store anomaly y-coordinates

    for idx, value in enumerate(data_stream_simulation()):
        data_x.append(idx)
        data_y.append(value)

        # Detect anomalies and add to anomaly lists
        if detector.update_ema(value):
            anomaly_x.append(idx)
            anomaly_y.append(value)

        # Real-time plot update
        try:
            with fig.batch_update():
                fig.data[0].x = list(data_x)
                fig.data[0].y = list(data_y)
                fig.data[1].x = list(anomaly_x)
                fig.data[1].y = list(anomaly_y)
        except Exception as e:
            print(f"Error updating visualization: {e}")
            continue

# --- Asynchronous Data Processing ---
async def process_data_stream():
    """
    Asynchronously process the data stream, detect anomalies, and print anomalies.
    """
    try:
        for value in data_stream_simulation():
            # Detect anomaly and print it
            if detector.update_ema(value):
                print(f"Anomaly detected: {value}")
            await asyncio.sleep(0.1)  # Simulate real-time non-blocking sleep
    except Exception as e:
        print(f"Error in processing data stream: {e}")

# --- Running the solution ---
detector = EMAAnomalyDetector(alpha=0.1, threshold=3)

# Start the event loop for real-time visualization and data processing
loop = asyncio.get_event_loop()
tasks = [loop.create_task(live_visualization()), loop.create_task(process_data_stream())]
loop.run_until_complete(asyncio.wait(tasks))

