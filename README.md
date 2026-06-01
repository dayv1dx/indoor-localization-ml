# 📍 Indoor Localization System using Machine Learning

This repository contains an end-to-end **Indoor Positioning System (IPS)** developed as my Undergraduate Thesis. The system leverages **Bluetooth Low Energy (BLE)** signals, **IoT hardware**, and **Machine Learning** to achieve high-precision coordinate prediction in indoor environments.


## 🏗️ System Architecture

The project is split into an offline data collection phase and an online real-time deployment phase:
* **Hardware:** 3 ESP32 modules acting as Access Points (APs) and 1 ESP32 acting as a Beacon.
* **Environment:** A grid discretized into 24 distinct zones for fingerprinting mapping.