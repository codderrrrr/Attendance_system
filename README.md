# Attendance System Using Face Recognition

## Overview
This is a **Face Recognition-based Attendance System** built using **Streamlit** and **face_recognition** library. The system allows users to **register**, **log in**, and **view attendance records**.

**Key Features:**
- Face recognition-based login and attendance marking.
- User registration via file upload or camera.
- Attendance records stored in text files.
- Simple and interactive **Streamlit UI**.

## 🛠️ Installation
### Prerequisites:
Ensure you have Python installed (>=3.7) and **git** installed.

### Clone the Repository:
```bash
git clone https://github.com/codderrrrr/Attendance_system.git
cd Attendance_system
```

### Install Required Dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 How to Run
Start the Streamlit application:
```bash
streamlit run app.py
```

## Features
### 1️⃣ **Home Page**
- Register as a new user
- Log in using face recognition
- View attendance records

### 2️⃣ **User Registration**
- Enter personal details (name, roll number, degree, section)
- Choose registration method:
  - Upload an image file
  - Capture a photo using the webcam

### 3️⃣ **Log In (Face Recognition)**
- Capture an image using a webcam
- Face is matched with the stored dataset
- If recognized, attendance is marked
- If unrecognized, the user is prompted to register

### 4️⃣ **View Attendance Records**
- Users can enter their name to check past attendance records

## Deployment on Streamlit Cloud
To deploy on **Streamlit Cloud**:
1. Push your repository to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Select your GitHub repo and deploy.
4. Ensure required dependencies are in `requirements.txt`.

## Project Structure
```
Attendance_system/
│── dataset/
│   ├── known/  # Stores registered user images
│   ├── unknown/  # Stores temp images for face matching
│── attendance/  # Stores attendance records as text files
│── app.py  # Main Streamlit application
│── requirements.txt  # Required Python libraries
│── README.md  # Project documentation
```

## License
This project is licensed under the **MIT License**.

## Acknowledgments
- This project uses the [face_recognition](https://github.com/ageitgey/face_recognition) library by **Adam Geitgey**, licensed under the MIT License.

