# **Efficient Data Stream Anomaly Detection**

## **Project Overview**
This project focuses on real-time anomaly detection in a continuous data stream using an Exponential Moving Average (EMA)-based approach. The data stream simulates real-world metrics, such as financial transactions or system performance metrics, with seasonal elements, noise, and random anomalies injected at intervals.

### **Key Features**
- **Real-time Anomaly Detection**: Detects deviations or anomalies in the data stream based on EMA and Z-scores.
- **Real-time Visualization**: Provides live plotting of the data stream along with flagged anomalies using Plotly.
- **Optimized for Streaming Data**: Efficient memory usage and non-blocking data processing using Python's `asyncio`.
- **Error Handling**: Robust error handling and data validation mechanisms to ensure smooth data flow.

## **Installation**
To run this project, install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

## **Requirements**
- Python 3.x
- Plotly
- Numpy

## **Running the Project**
To start anomaly detection and visualization in real-time, run the following command in your terminal:

```bash
python anomaly_detection.py
```

## **Explanation of Chosen Algorithm: EMA for Anomaly Detection**
- **Exponential Moving Average (EMA)** is chosen because it is highly suitable for **real-time anomaly detection** in streaming data. EMA gives more weight to recent data points, making it adaptive to **concept drift** and changes in the data stream over time.
  
- **Z-score** is calculated to detect anomalies. If the Z-score exceeds a certain **threshold**, the point is flagged as an anomaly. This approach is robust to **seasonal variations** and noise, which are often present in real-world data.

### **Optimizations and Considerations**
1. **Batch Update**: The visualization updates in batches instead of after every point, reducing rendering overhead.
2. **Deque**: The use of `deque` ensures we only store the last 200 data points, conserving memory.
3. **Asynchronous Processing**: `asyncio` ensures that data streaming, anomaly detection, and visualization are processed simultaneously without blocking each other.

### **Error Handling**
- **Custom Exceptions**: Introduced `DataStreamException` to handle invalid data entries.
- **ZeroDivisionError**: Handled gracefully in case of any division by zero during anomaly calculations.

## **Code Explanation**
- **data_stream_simulation()**: Simulates a continuous stream of data with a seasonal pattern, noise, and random anomalies.
- **EMAAnomalyDetector**: Implements EMA for real-time anomaly detection. It computes the EMA and standard deviation of incoming data points and flags any outliers based on Z-scores.
- **live_visualization()**: Uses Plotly for real-time plotting of the data stream and marks anomalies with red dots.
- **Error Handling**: Ensures robust data validation and exception handling to prevent crashes.

## **License**
This project is open-source and licensed under the MIT License.

