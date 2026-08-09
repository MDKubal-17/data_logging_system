# VITAL-CORE — Data Logging System for Physiological Parameters

VITAL-CORE is a real-time physiological data logging and monitoring system that integrates **embedded systems, Python-based data processing, visualization, networking, and Artificial Intelligence**.

The system is designed to acquire and log important physiological parameters such as **Heart Rate (HR), Blood Pressure (BP), SpO₂, Body Temperature, and Respiratory Rate (RR)**. It provides real-time visualization, automated alerts, AI-generated clinical summaries, and voice-based access to stored patient data.

> **Note:** VITAL-CORE is a prototype developed for academic and research purposes. It is not intended to replace certified medical devices or provide clinical diagnosis.

## ✨ Features

* 📊 Real-time physiological parameter monitoring
* ❤️ Heart Rate monitoring
* 🩸 Blood Pressure acquisition using TTL-V3 Digital BP Sensor
* 🫁 SpO₂ and Respiratory Rate monitoring
* 🌡️ Body Temperature monitoring
* 📁 Automatic CSV-based data logging
* 📈 Real-time graphical visualization
* 💓 Synthetic ECG waveform generation using Gaussian PQRST modeling
* 🚨 Automatic threshold-based emergency detection
* 📡 UDP-based emergency alert communication
* 🤖 AI-powered clinical trend summarization using Gemini
* 🎙️ Voice-based patient data retrieval using Groq and Text-to-Speech
* 🔌 UART-based communication between MCU and host system
* 🧵 Multi-threaded data acquisition and processing
* ⚡ Sensor disconnection and missing-data handling
* 🔋 Dual-power strategy for improved hardware stability

## 🏗️ System Architecture

VITAL-CORE follows a three-tier architecture:

```text
┌──────────────────────────────┐
│       ACQUISITION LAYER      │
│                              │
│  TM4C123GXL / ARM Cortex-M4F │
│  └── Physiological Sensors   │
│  └── BP Sensor               │
│  └── UART Communication      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       PROCESSING LAYER       │
│                              │
│  Python Multi-threaded Engine│
│  └── UART Data Ingestion     │
│  └── Data Processing         │
│  └── CSV Logging             │
│  └── Real-time GUI           │
│  └── ECG Simulation          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   INTELLIGENCE & NETWORKING  │
│                              │
│  └── Gemini AI Summary       │
│  └── Groq Voice Retrieval    │
│  └── UDP Emergency Alerts    │
│  └── Nurse Station           │
└──────────────────────────────┘
```

The project separates low-level hardware acquisition from data processing and higher-level intelligent analysis to maintain responsiveness and data integrity.

## 🔧 Hardware

### Main Components

* **TM4C123GXL Tiva C LaunchPad**

  * ARM Cortex-M4F microcontroller
* **TTL-V3 Digital Blood Pressure Sensor**
* USB connection
* External battery / 5V supply for the BP pump
* Required wiring and connectors

### UART Configuration

| Interface | Pins     | Purpose                    | Baud Rate |
| --------- | -------- | -------------------------- | --------: |
| UART0     | PA0, PA1 | Communication with host PC |    115200 |
| UART1     | PB0, PB1 | Blood Pressure Sensor      |      9600 |
| GPIO      | PA5      | BP pump trigger            |         — |

The hardware uses separate logic and actuator power rails to isolate the high-current BP pump from the MCU logic circuitry.

## 💻 Software Stack

| Technology | Purpose                                |
| ---------- | -------------------------------------- |
| Python     | Main application and processing engine |
| Tkinter    | Graphical User Interface               |
| Matplotlib | Real-time physiological plotting       |
| NumPy      | Numerical processing                   |
| Pandas     | CSV data handling                      |
| PySerial   | UART communication                     |
| Gemini API | AI-based clinical summarization        |
| Groq API   | Voice/data retrieval                   |
| Pyttsx3    | Text-to-Speech                         |
| UDP        | Emergency alert communication          |

The software uses multiple threads to separate GUI rendering, serial data acquisition, and emergency handling, helping maintain a responsive dashboard.

## 📊 Monitored Parameters

| Parameter        | Normal Range | Alert Condition     |
| ---------------- | ------------ | ------------------- |
| Heart Rate       | 60–100 BPM   | < 60 or > 100       |
| SpO₂             | 95–100%      | < 95%               |
| Respiratory Rate | 12–20 RPM    | < 12 or > 20        |
| Blood Pressure   | 120/80 mmHg  | Systolic > 140      |
| Temperature      | 36.5–37.5 °C | < 36.5 or > 37.5 °C |

These thresholds are used by the monitoring and emergency alert logic.

## 🤖 AI Integration

VITAL-CORE contains two AI-assisted modules:

### Clinical AI Summary

The system uses the **Gemini-2.5-Flash API** to analyze recent patient records and generate a longitudinal summary of physiological trends.

### Voice Assistant

The system uses **Groq** for rapid voice-query processing. Users can request information from the locally stored CSV records through voice, and **Pyttsx3** provides the spoken response.

## 💓 Synthetic ECG

The project includes a synthetic ECG generation module based on **Gaussian PQRST modeling**.

The generated waveform represents:

* P Wave
* QRS Complex
* T Wave

The waveform is synchronized with the current heart rate. The system can classify rhythm into:

* Normal Sinus Rhythm
* Tachycardia
* Bradycardia
* Atrial Fibrillation

This ECG is intended for visualization and simulation rather than direct clinical diagnosis.

## 📁 Data Logging

Physiological measurements are stored locally in:

```text
patient data.csv
```

The CSV file acts as the persistent data source for historical analysis, AI summarization, and voice-based data retrieval.

## 🚨 Emergency Alert System

When a monitored physiological parameter crosses its defined threshold:

```text
Sensor Data
     ↓
Data Processing
     ↓
Threshold Checking
     ↓
Abnormal Value Detected
     ↓
Emergency Handler
     ↓
UDP Alert
     ↓
Remote Nurse Station
```

The system also provides visual emergency notifications through the monitoring dashboard.

## 🧪 Testing

The system was validated using multiple test scenarios, including:

* High BP detection
* BP sensor trigger operation
* AI clinical summarization
* Voice assistance
* CSV data persistence
* UART disconnection handling

All listed validation test cases in the project report were marked as **Pass**.

## 🚀 Future Scope

Possible future improvements include:

* Custom PCB development
* Wearable implementation
* Bluetooth Low Energy (BLE) / Wi-Fi communication
* Multi-lead ECG integration
* Blood glucose monitoring
* Advanced sensor fusion
* Digital signal filtering
* Deep-learning-based predictive diagnostics
* Cloud-based healthcare dashboard
* Telemedicine integration
* Remote doctor monitoring
* HL7-based healthcare data interoperability
* LoRa-based rural healthcare telemetry

The report specifically identifies hardware miniaturization, additional sensors, predictive analytics, and cloud/telemedicine integration as major future directions.

## 👩‍💻 Team

**Project:** Data Logging System for Physiological Parameters — VITAL-CORE

**Team Members:**

* Divya Manohar Gurav
* Anwesha Jana
* Maithilee Dhananjay Kubal

**Guide:** Prof. Sudhakar Yerme

**Institution:** Usha Mittal Institute of Technology, S.N.D.T. Women's University, Mumbai

## 📚 Project Documentation

The complete project report contains:

* Introduction and research motivation
* Literature review
* System architecture
* Hardware interfacing
* Software methodology
* Data processing pipeline
* AI integration
* System validation
* UML diagrams
* Data Flow Diagrams
* Implementation details
* Conclusion and future scope

## ⚠️ Disclaimer

VITAL-CORE is an **academic prototype** developed for educational and research purposes. It is not a certified medical device and should not be used as a substitute for professional medical equipment, diagnosis, or treatment.

## 📄 License

This project is developed as an academic project.
Add an appropriate open-source license if the project is intended for public distribution.
