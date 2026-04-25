import streamlit as st
from datetime import date
import os

# Try importing OpenAI safely
try:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else None
except:
    client = None

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Study Planner", layout="wide")

# ------------------ UI FIX ------------------
st.markdown("""
<style>
.stApp { background-color: #ffffff; }

.main, .block-container {
    color: #111827 !important;
}

h1, h2, h3 {
    color: #111827 !important;
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
    if not client:
        return "⚠ AI feature not available. Please add your OPENAI_API_KEY."

    prompt = f"""
    Create a simple and clear day-wise study plan.

    Subjects: {subjects}
    Study hours per day: {hours}
    Days left: {days}
    Weak areas: {weak}

    Keep it structured and easy to follow.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a study planner."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ AI Error: {str(e)}"

# ------------------ GENERATE ------------------
if st.sidebar.button("🚀 Generate Plan"):

    if subjects.strip() == "":
        st.warning("⚠ Please enter subjects")
    else:
        days_left = (exam_date - date.today()).days

        if days_left <= 0:
            st.error("❌ Exam date must be in future")
        else:
            st.subheader("📅 Your Study Plan")

            with st.spinner("Generating plan..."):
                plan = generate_ai_plan(subjects, hours, days_left, weak_areas)

            st.write(plan)

            st.download_button(
                "📥 Download Plan",
                plan,
                file_name="study_plan.txt"
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
st.header("💡 Study Tips")

st.success("""
✔ Focus on weak areas  
✔ Revise daily  
✔ Practice problems  
✔ Take breaks  
""")
             
