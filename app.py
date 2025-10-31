import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 📁 Attendance file name
ATTENDANCE_FILE = "attendance.csv"

# 🧩 Helper: Load attendance data
def load_attendance():
    if os.path.exists(ATTENDANCE_FILE):
        return pd.read_csv(ATTENDANCE_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Date", "Time", "Status"])

# 🧩 Helper: Save attendance data
def save_attendance(data):
    data.to_csv(ATTENDANCE_FILE, index=False)

# 🧩 Helper: Mark attendance manually
def mark_attendance(name):
    data = load_attendance()
    today = datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.now().strftime("%H:%M:%S")

    if not ((data["Name"] == name) & (data["Date"] == today)).any():
        new_entry = pd.DataFrame([[name, today, time_now, "Present"]],
                                 columns=["Name", "Date", "Time", "Status"])
        data = pd.concat([data, new_entry], ignore_index=True)
        save_attendance(data)
        st.success(f"✅ Attendance marked for {name}")
    else:
        st.warning(f"⚠️ {name} is already marked present today!")

# 🏠 Streamlit App Layout
st.set_page_config(page_title="AI Attendance System", layout="centered")

st.title("🧠 AI-Based Attendance System (Demo)")
st.caption("Simplified version for deployment without camera or face recognition")

# Sidebar options
menu = ["🏠 Home", "🧍 Register Face", "📋 View Attendance"]
choice = st.sidebar.radio("Navigation", menu)

# --------------- HOME ---------------
if choice == "🏠 Home":
    st.image(
        "https://cdn.pixabay.com/photo/2023/02/22/18/00/artificial-intelligence-7807048_1280.jpg",
        caption="AI-based Attendance System", use_container_width=True)
    st.markdown("""
    ### Welcome to Smart Attendance System 👋  
    - This is a **deployable version** (without camera).
    - You can **manually mark attendance** and **view records**.
    """)

# --------------- REGISTER FACE (manual) ---------------
elif choice == "🧍 Register Face":
    st.header("Register a New Student/Person")

    name = st.text_input("Enter Name")
    if st.button("Register Face"):
        if name.strip() == "":
            st.error("Please enter a valid name!")
        else:
            # In full version, camera would register the face.
            st.success(f"🧍 Face registered for: {name}")
            st.info("Camera features disabled for cloud deployment.")

# --------------- VIEW ATTENDANCE ---------------
elif choice == "📋 View Attendance":
    st.header("Attendance Records")

    data = load_attendance()
    if data.empty:
        st.warning("No attendance records found!")
    else:
        st.dataframe(data)

        # Option to manually mark attendance
        st.subheader("Manually Mark Attendance")
        name = st.text_input("Enter Name to Mark Present")
        if st.button("Mark Attendance"):
            if name.strip() == "":
                st.error("Please enter a valid name!")
            else:
                mark_attendance(name)

        # Option to clear data
        if st.button("Clear All Records"):
            os.remove(ATTENDANCE_FILE)
            st.success("All attendance records cleared!")
