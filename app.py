import streamlit as st
from datetime import date
import os

# Optional AI
try:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else None
except:
    client = None

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Study Planner", layout="wide")

# ------------------ PERFECT VISIBILITY FIX ------------------
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color: #ffffff;
}

/* FORCE ALL TEXT DARK */
html, body, [class*="css"]  {
    color: #111111 !important;
}

/* HEADINGS */
h1, h2, h3 {
    color: #111111 !important;
    font-weight: bold;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #0f172a !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* BUTTONS */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 230px;
    font-size: 18px;
}

/* DOWNLOAD BUTTON */
.stDownloadButton>button {
    background-color: #16a34a;
    color: white;
}

/* INPUTS */
input, textarea {
    color: #111111 !important;
    background-color: #f9fafb !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("📚 AI Study Planner Pro")

# ------------------ SIDEBAR ------------------
st.sidebar.header("📥 Enter Details")

subjects = st.sidebar.text_input("📘 Subjects")
hours = st.sidebar.slider("⏱ Study hours/day", 1, 12, 4)
exam_date = st.sidebar.date_input("📅 Exam Date", min_value=date.today())
weak_areas = st.sidebar.text_area("⚠ Weak Areas")

# ------------------ AI FUNCTION ------------------
def generate_ai(subjects, hours, days, weak):
    if not client:
        return "⚠ AI not enabled (add API key)"

    prompt = f"""
    Create a day-wise study plan.
    Subjects: {subjects}
    Hours: {hours}
    Days: {days}
    Weak areas: {weak}
    """

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a study planner."},
                {"role": "user", "content": prompt}
            ]
        )
        return res.choices[0].message.content
    except:
        return "❌ AI error"

# ------------------ GENERATE PLAN ------------------
if st.sidebar.button("🚀 Generate Plan"):

    if subjects.strip() == "":
        st.warning("Enter subjects")
    else:
        days_left = (exam_date - date.today()).days

        if days_left <= 0:
            st.error("Invalid exam date")
        else:
            st.subheader("📅 Study Plan")

            with st.spinner("Generating..."):
                plan = generate_ai(subjects, hours, days_left, weak_areas)

            st.write(plan)

            st.download_button("📥 Download Plan", plan)

# ------------------ DAILY GOAL TRACKER ------------------
st.header("🎯 Daily Goal Tracker")

goal = st.text_input("Enter today's goal")

if "goals" not in st.session_state:
    st.session_state.goals = []

if st.button("Add Goal"):
    if goal:
        st.session_state.goals.append({"goal": goal, "done": False})

for i, g in enumerate(st.session_state.goals):
    st.session_state.goals[i]["done"] = st.checkbox(
        g["goal"], value=g["done"]
    )

# ------------------ PROGRESS ------------------
st.header("📊 Progress Tracker")

completed = sum(g["done"] for g in st.session_state.goals)
total = len(st.session_state.goals)

if total > 0:
    percent = completed / total
    st.write(f"Completed: {completed}/{total}")
    st.progress(percent)

    # Simple chart
    st.bar_chart({"Progress": [completed, total - completed]})
else:
    st.write("No goals added")

# ------------------ SMART TIPS ------------------
st.header("💡 Smart Tips")

st.success("""
✔ Study consistently  
✔ Focus on weak areas  
✔ Revise daily  
✔ Take breaks  
✔ Practice questions  
""")
