# 🧑‍💻 Face Recognition Based Attendance System

## 📝 Overview

This project is a Face Recognition Based Attendance System that automates attendance marking using facial recognition technology. It uses OpenCV for face detection and recognition, and stores attendance records in CSV files.

---

## ✨ Features

- 🕵️ Real-time face detection and recognition
- 🕒 Automatic attendance marking with date and time
- 📄 Stores attendance records in CSV format
- 🧑‍🎓 Student registration and training
- 🖼️ Uses Haar Cascade for face detection

---

## 📁 Directory Structure

```
Face_recognition_based_attendance_system-master/
│
├── haarcascade_frontalface_default.xml      # Haar Cascade for face detection
├── main.py                                 # Main application script
├── Attendance/                             # Stores daily attendance CSV files
│   └── Attendance_14-06-2025.csv
├── StudentDetails/                         # Stores student details
│   └── StudentDetails.csv
├── TrainingImage/                          # Stores captured images for training
└── TrainingImageLabel/                     # Stores training labels and model
    ├── psd.txt
    └── Trainner.yml
```

---

## 🚀 Getting Started

### Prerequisites

- 🐍 Python 3.x
- 🖼️ OpenCV
- 🔢 NumPy
- 📊 Pandas

Install dependencies using:
```
pip install opencv-python numpy pandas
```

---

### ▶️ Usage

1. **Register Students:**  
   Run `main.py` and use the interface to register new students. Images will be saved in `TrainingImage/`.

2. **Train Model:**  
   Train the model after registration. The trained model is saved in `TrainingImageLabel/Trainner.yml`.

3. **Mark Attendance:**  
   Use the attendance feature to recognize faces and mark attendance in the `Attendance/` folder.

4. **View Attendance:**  
   Open the relevant CSV file in the `Attendance/` folder to view attendance records.

---

## 📊 Attendance File Format

Attendance files (e.g., `Attendance_14-06-2025.csv`) have the following columns:

| 🆔 Id | 👤 Name | 📅 Date | ⏰ Time |
|-------|--------|---------|---------|

, 