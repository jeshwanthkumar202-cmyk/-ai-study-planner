import streamlit as st
from datetime import date

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Study Planner", layout="wide")

# ------------------ STYLE ------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        height: 40px;
        width: 200px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("📚 AI Personalized Study Planner")

# ------------------ INPUT ------------------
st.header("📝 Enter Your Study Details")

subjects = st.text_input("Subjects (comma separated)")
hours = st.slider("Study hours per day", 1, 12, 4)
exam_date = st.date_input("Exam Date", min_value=date.today())
weak_areas = st.text_area("Weak Areas (optional)")

# ------------------ GENERATE PLAN ------------------
if st.button("Generate Study Plan"):

    if subjects.strip() == "":
        st.warning("Please enter subjects")
    else:
        subject_list = [s.strip() for s in subjects.split(",") if s.strip()]

        days_left = (exam_date - date.today()).days

        if days_left <= 0:
            st.error("Exam date must be in the future")
        else:
            st.subheader("📅 Your Personalized Plan")

            per_subject_time = max(1, hours // len(subject_list))

            for day in range(1, days_left + 1):
                st.markdown(f"### Day {day}")
                for sub in subject_list:
                    st.write(f"📘 {sub} → {per_subject_time} hrs")

            if weak_areas:
                st.subheader("⚠ Focus More On")
                st.write(weak_areas)

            st.success("✅ Study Plan Generated!")

# ------------------ PROGRESS TRACKER ------------------
st.header("📈 Progress Tracker")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

task = st.text_input("Add completed topic")

if st.button("Add Task"):
    if task:
        st.session_state.tasks.append(task)

for t in st.session_state.tasks:
    st.write(f"✅ {t}")

# ------------------ STUDY TIPS ------------------
st.header("💡 Smart Study Tips")

st.info("""
- Study daily with consistency  
- Revise every 2–3 days  
- Focus more on weak areas  
- Take short breaks (Pomodoro technique)  
""")
