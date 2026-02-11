# 🚤 Scavenger Boat  
## AI-Powered Trash Collecting Boat Using Faster R-CNN

---

## 📖 Overview

The **Scavenger Boat** is an autonomous water-cleaning robotic system designed to detect and collect floating waste using deep learning and embedded hardware integration.

The system uses a **Faster R-CNN object detection model** to identify floating debris in real time. Upon detection, a motorized conveyor mechanism activates to collect the waste efficiently.

Inspired by IEEE research on autonomous water-cleaning robots, this project integrates AI-based vision, obstacle avoidance, and renewable energy support into a scalable and low-cost solution for water pollution control.

---

## 🚀 Key Features

- 🧠 **AI-Based Detection:** Faster R-CNN model for real-time trash identification.
- 🚤 **Autonomous Navigation:** Dual-motor propulsion with ultrasonic obstacle avoidance.
- ♻️ **Smart Collection System:** Conveyor activates only when trash is detected.
- 🔋 **Solar-Assisted Power:** Li-ion battery with optional solar panel charging.
- 🧩 **Modular Architecture:** Independent vision, navigation, motor, and power modules.

---

## 🛠 Tech Stack

### 🔩 Hardware
- Raspberry Pi 5
- PiCamera v3
- HC-SR04 Ultrasonic Sensor
- L298N / IBT-2 Motor Driver
- Propeller Motors
- Conveyor Belt Mechanism
- Li-ion Battery
- Solar Panel (Optional)

### 💻 Software
- Python 3.9+
- PyTorch
- TorchVision
- OpenCV
- Picamera2
- RPi.GPIO

---

## ⚙️ System Architecture

1. PiCamera captures live video feed.
2. Faster R-CNN model processes frames to detect floating waste.
3. If trash is detected:
   - Conveyor motor activates.
   - Boat aligns and collects waste.
4. Ultrasonic sensor prevents collisions.
5. System runs on battery with optional solar recharging.

---

## 🌍 Applications

- River and lake cleaning
- Smart city environmental systems
- Automated water body maintenance
- Sustainable pollution control

---

## 📌 Future Improvements

- GPS-based real-time tracking
- Edge-optimized lightweight detection model
- IoT dashboard for monitoring
- Fully autonomous path planning

---

## 👩‍💻 Author

**Dikshitha Ramesh**

---

## 📜 License

This project is licensed under the MIT License.
