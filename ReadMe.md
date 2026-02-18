# ⚡ CPE-Pulse: The Engineering Data Analysis Hub

![Status](https://img.shields.io/badge/Status-Active_Development-green)
![Platform](https://img.shields.io/badge/Platform-Web_|_Mobile-blue)
![Tech Stack](https://img.shields.io/badge/Built_With-Python_|_Streamlit_|_Pandas-orange)

## 📖 Overview
**CPE-Pulse** is an open-source, interactive learning platform built for Computer Engineering (CpE) students. 

Traditional data science courses focus on finance or sales data. **CPE-Pulse** focuses on **Engineering Data**: analyzing network packets, sensor noise, power consumption, and circuit tolerances. This project is designed to be fully responsive, allowing students to visualize data and learn concepts directly from their mobile phones or laptops.

## 🎯 Project Goals
1.  **Bridge the Gap:** Connect abstract statistical concepts (Standard Deviation, Variance) to practical Engineering use cases (Quality Control, Signal Processing).
2.  **Mobile-First Learning:** Provide accessible, bite-sized lessons that work on any device.
3.  **Interactive Tooling:** Allow users to upload raw `.csv` or `.log` files (e.g., from Wireshark or Arduino) and see instant visualizations.

## 🛠 Features (Planned)

### 📡 Module 1: Network Traffic Analyzer
* **Input:** Upload a CSV export of network logs.
* **Learn:** How to calculate throughput, identify latency spikes, and visualize packet loss over time.
* **Visual:** Interactive heatmaps of network congestion.

### 🤖 Module 2: Robotics & Sensor Fusion
* **Input:** Accelerometer or Gyroscope data.
* **Learn:** Cleaning "noisy" sensor data using Moving Averages and Kalman Filters.
* **Visual:** "Before vs. After" filtering graphs.

### 🔋 Module 3: Power & Performance (Lean Six Sigma)
* **Input:** Voltage/Current logs from embedded systems.
* **Learn:** Using Control Charts (SPC) to monitor hardware stability and battery drain.
* **Visual:** Pareto charts showing top power-consuming processes.

## 🚀 Tech Stack
* **Core Engine:** Python 3.9+
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly (for interactive mobile charts), Matplotlib
* **Web Framework:** Streamlit (chosen for rapid mobile-responsive deployment)

## 📱 How to Run (Local Development)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/CPE-Pulse.git](https://github.com/your-username/CPE-Pulse.git)