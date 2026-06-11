# AtMarkAI - AI Powered Attendance Management System

## Overview

AtMarkAI is an AI-powered attendance management system designed to automate student attendance using facial recognition and voice verification technologies. The system eliminates manual attendance processes and provides a secure, efficient, and scalable solution for educational institutions.

The project combines computer vision, machine learning, and cloud database services to accurately identify students and record attendance in real time.

---

## Features

### Student Management

* Register and manage student profiles
* Store student information securely
* Maintain enrollment records

### Teacher Management

* Teacher authentication and authorization
* Subject and class management
* Attendance monitoring dashboard

### AI-Based Attendance

* Face detection and recognition
* Face embedding generation using Dlib
* Student identification using Machine Learning models
* Real-time attendance marking

### Voice Verification

* Speaker recognition using Resemblyzer
* Additional identity verification layer
* Improved attendance security

### Attendance Tracking

* Automatic attendance recording
* Attendance history and reports
* Subject-wise attendance monitoring

### Cloud Database Integration

* Secure storage using Supabase
* Real-time data synchronization
* Centralized attendance records

---

## System Architecture

```text
Camera Input
      │
      ▼
Face Detection
      │
      ▼
Face Embedding Extraction (Dlib)
      │
      ▼
Student Classification (SVM)
      │
      ▼
Voice Verification (Resemblyzer)
      │
      ▼
Attendance Validation
      │
      ▼
Supabase Database
      │
      ▼
Dashboard & Reports
```

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Machine Learning & AI

* Dlib
* OpenCV
* Scikit-Learn
* NumPy
* Resemblyzer

### Database

* Supabase

### Authentication

* Supabase Authentication

---

## Database Schema

### Teachers

Stores teacher information and credentials.

### Students

Stores student details and face embeddings.

### Subjects

Contains subject information.

### Enrollment

Maps students to subjects.

### Attendance Logs

Stores attendance records with timestamps.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/AtMarkAI.git
cd AtMarkAI
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

---

## Running the Application

```bash
streamlit run app.py
```

---

## Machine Learning Pipeline

### Face Recognition

1. Capture student images
2. Detect faces using Dlib/OpenCV
3. Generate face embeddings
4. Train SVM classifier
5. Predict student identity during attendance

### Voice Recognition

1. Record voice samples
2. Generate voice embeddings using Resemblyzer
3. Compare embeddings during attendance verification
4. Validate student identity

---

## Future Enhancements

* Multi-camera attendance support
* Real-time notifications
* Attendance analytics dashboard
* Deep learning-based face recognition
* QR code backup attendance system

---

## Project Goals

* Reduce manual attendance effort
* Improve attendance accuracy
* Prevent proxy attendance
* Provide scalable attendance management
* Integrate AI technologies into educational systems

---

## Author

Nitish Kumar

B.Tech AI & ML Student

AtMarkAI was developed as an academic and practical AI project to demonstrate the application of Computer Vision, Machine Learning, Voice Biometrics, and Cloud Technologies in real-world attendance management systems.
