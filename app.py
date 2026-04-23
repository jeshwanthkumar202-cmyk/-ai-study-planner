import streamlit as st
from datetime import date
import os
from openai import OpenAI

# ------------------ API SETUP ------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Study Planner", layout="wide")

# ------------------ UI FIX ------------------
st.markdown("""
<style>
.stApp { background-color: #ffffff; }
.main, .block-container { color: #111827 !important; }

h1, h2, h3 { color: #111827 !important; }

p, label, div {
    color: #111827 !important;
    font-size: 18px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a !important;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Buttons */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 230px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("🤖 AI Personalized Study Planner")

# ------------------ SIDEBAR ------------------
st.sidebar.header("📥 Enter Details")

subjects = st.sidebar.text_input("📘 Subjects (comma separated)")
hours = st.sidebar.slider("⏱ Study hours/day", 1, 12, 4)
exam_date = st.sidebar.date_input("📅 Exam Date", min_value=date.today())
weak_areas = st.sidebar.text_area("⚠ Weak Areas")

# ------------------ AI FUNCTION ------------------
def generate_ai_plan(subjects, hours, days, weak):
    prompt = f"""
    Create a detailed day-wise study plan.

    Subjects: {subjects}
    Study hours per day: {hours}
    Days left: {days}
    Weak areas: {weak}

    Make it structured, clear, and easy to follow.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful study planner assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# ------------------ GENERATE ------------------
if st.sidebar.button("🚀 Generate AI Plan"):

    if subjects.strip() == "":
        st.warning("⚠ Please enter subjects")
    else:
        days_left = (exam_date - date.today()).days

        if days_left <= 0:
            st.error("❌ Exam date must be in the future")
        else:
            with st.spinner("🤖 AI is generating your plan..."):
                plan = generate_ai_plan(subjects, hours, days_left, weak_areas)

            st.subheader("📅 Your AI Study Plan")
            st.write(plan)

            # DOWNLOAD
            st.download_button(
                label="📥 Download Plan",
                data=plan,
                file_name="ai_study_plan.txt",
                mime="text/plain"
            )

# ------------------ PROGRESS TRACKER ------------------
st.header("📈 Progress Tracker")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

task = st.text_input("✍ Add Completed Topic")

if st.button("➕ Add Progress"):
    if task:
        st.session_state.tasks.append({"task": task, "done": False})

for i, t in enumerate(st.session_state.tasks):
    st.session_state.tasks[i]["done"] = st.checkbox(
        f"✅ {t['task']}", value=t["done"]
    )

# ------------------ SUMMARY ------------------
st.header("📊 Progress Summary")

completed = sum(t["done"] for t in st.session_state.tasks)
total = len(st.session_state.tasks)

if total > 0:
    st.write(f"Completed: {completed}/{total}")
    st.progress(completed / total)
else:
    st.write("No tasks yet")

# ------------------ TIPS ------------------
st.header("💡 AI Study Tips")

st.success("""
✔ Focus on weak areas first  
✔ Revise daily  
✔ Practice questions  
✔ Take breaks  
""")
