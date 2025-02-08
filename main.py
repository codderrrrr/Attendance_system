import subprocess
from datetime import datetime
from PIL import Image
import face_recognition
import face_recognition_models
import cv2
import streamlit as st
from streamlit import session_state
import os
from streamlit_option_menu import option_menu

data_path = './dataset/known'
unknown_data = './dataset/unknown'
attendance_path = './attendance'

if "page" not in session_state:
    st.session_state.page = "home"
if "user_data" not in session_state:
    st.session_state.user_data = {}

def change_page(page):
    st.session_state.page = page

st.markdown("""
    <style>
        .stButton > button {
            width: 100%;
            height: 60px;
            border-radius: 12px;
            font-size: 18px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #4CAF50;
            color: white;
        }
        .stTitle {
            text-align: center;
            font-size: 40px;
            color: #330;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

if st.session_state.page=="home":
    st.title('Attendance system')
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button('Register'):
            st.session_state.page = "register"
    with col2:
        if st.button('Log in'):
            st.session_state.page = "log in"
    col3, col4, col5 = st.columns([2, 1, 2])
    with col4:
        if st.button('Records'):
            st.session_state.page = "records"

elif st.session_state.page=="register":
    first_name = st.text_input('First Name')
    last_name = st.text_input('Last Name')
    roll_no = st.text_input('Roll no:')
    program = st.text_input('Enter your degree program:')
    section = st.selectbox('Enter section', ['A','B','C','D'])
    action = st.selectbox('how do you want to register: ', ['Upload file', 'Camera'])
    if st.button('Enter'):
        if not first_name or not last_name or not roll_no or not program or not section:
            st.error("Please fill the required field")
        else:
            st.session_state.user_data = {"first_name": first_name, "last_name": last_name}
            text_file = f"{first_name}_{last_name}.txt"
            with open(os.path.join(data_path, text_file), 'w') as f:
                f.write(f"First Name: {first_name}\n")
                f.write(f"Last Name: {last_name}\n")
                f.write(f"Roll No: {roll_no}\n")
                f.write(f"Class: {program}-{section}\n")
            change_page(action.lower())

elif  st.session_state.page=="log in":
    st.title("Log in")
    camera_input = st.camera_input('Capture your photo')
    if st.button('Submit'):
        if camera_input:
            img_file = "temp.jpg"
            image = Image.open(camera_input)
            image.save(os.path.join(unknown_data, img_file))
            output = subprocess.check_output(['face_recognition', data_path, os.path.join(unknown_data, img_file)])
            output = output.decode('utf-8')
            output = output.split(',')[1].strip()

            if output!='no_persons_found' and output!='unknown_person':
                current_date = datetime.now()
                today_time = f"{current_date.day}/{current_date.month}/{current_date.year}"
                user_attendance_file = os.path.join(attendance_path, f"{output}.txt")

                with open(user_attendance_file, 'r') as f:
                    attendance_record = f.readlines()
                    if any(today_time in record for record in attendance_record):
                        st.warning('You have already marked you attendance for today.')
                        st.stop()

                with open(user_attendance_file, 'a') as f:
                    f.write(f'{output.replace('_', ' ')} present on {today_time}\n')
                st.text(f'{output.replace('_', ' ')} attendance marked')
                change_page('home')
            else:
                st.error('User not found in database. Register first.')
        else:
            st.error('Upload image')

elif  st.session_state.page=="records":
    st.title("Attendance records")
    first_n = st.text_input('First Name')
    last_n = st.text_input('Last Name')
    name = f"{first_n}_{last_n}.txt"
    file_name = os.path.join(attendance_path, name)

    if st.button("View attendance record"):
        if first_n and last_n:
            try:
                with open (file_name, 'r') as f:
                    records = f.readlines()
                    st.subheader(f"Attendance Records for {first_n} {last_n}")
                    for record in records:
                        st.write(record)
            except FileNotFoundError:
                st.error("The user is not in database.")
        else:
            st.error("Please enter first and last name.")

elif st.session_state.page=='upload file':
    st.text('Upload image')
    uploaded_file = st.file_uploader('Upload a photo', type='jpg')
    if st.button('Submit'):
        if uploaded_file is not None:
            first_name = st.session_state.user_data.get("first_name", "")
            last_name = st.session_state.user_data.get("last_name", "")
            image_file = f"{first_name}_{last_name}.jpg"
            image = Image.open(uploaded_file)
            image.save(os.path.join(data_path, image_file))
            st.image(image, caption="Uploaded Image", use_container_width=True)
            st.success(f"Image submitted! Image saved as {os.path.join(data_path, image_file)}")
            change_page('home')
        else:
            st.warning("Please upload image file.")

elif st.session_state.page=='camera':
    st.title("Upload image by Camera")
    camera_input = st.camera_input('Capture your photo')

    if st.button('Submit'):
        first_name = st.session_state.user_data.get("first_name", "")
        last_name = st.session_state.user_data.get("last_name", "")
        image_file = f"{first_name}_{last_name}.jpg"
        image = Image.open(camera_input)
        image.save(os.path.join(data_path, image_file))
        st.image(image, caption="Uploaded file", use_container_width=True)
        st.success(f"Image captured from camera and saved to {os.path.join(data_path, image_file)}")
        change_page('home')
