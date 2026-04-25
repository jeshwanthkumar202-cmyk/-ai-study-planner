import streamlit as st
from datetime import date
import os

# ------------------ OPTIONAL AI SETUP ------------------
try:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else None
except:
    client = None

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Study Planner Pro", layout="wide")

# ------------------ FULL UI + VISIBILITY FIX ------------------
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color: #ffffff;
}

/* FORCE TEXT DARK */
html, body, [class*="css"] {
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

/* INPUT FIX (IMPORTANT) */
input, textarea {
    color: #000000 !important;
    background-color: #ffffff !important;
    caret-color: #000000 !important;
}

/* PLACEHOLDER */
input::placeholder, textarea::placeholder {
    color: #6b7280 !important;
}

/* SIDEBAR INPUT */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
    background-color: #1e293b !important;
    color: white !important;
}

/* BUTTONS */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 240px;
    font-size: 18px;
}

/* DOWNLOAD BUTTON */
.stDownloadButton>button {
    background-color: #16a34a;
    color: white;
}

/* PROGRESS BAR */
.stProgress > div > div {
    background-color: #2563eb;
}

</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("📚 AI Study Planner Pro")

# ------------------ SIDEBAR INPUT ------------------
st.sidebar.header("📥 Enter Details")

subjects = st.sidebar.text_input("📘 Subjects (comma separated)")
hours = st.sidebar.slider("⏱ Study hours/day", 1, 12, 4)
exam_date = st.sidebar.date_input("📅 Exam Date", min_value=date.today())
weak_areas = st.sidebar.text_area("⚠ Weak Areas")

# ------------------ AI FUNCTION ------------------
def generate_ai_plan(subjects, hours, days, weak):
    if not client:
        return "⚠ AI not enabled. Add OPENAI_API_KEY to use AI."

    prompt = f"""
    Create a simple day-wise study plan.

    Subjects: {subjects}
    Hours per day: {hours}
    Days left: {days}
    Weak areas: {weak}

    Keep it clear and structured.
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
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

# ------------------ GENERATE PLAN ------------------
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

# ------------------ DAILY GOALS ------------------
st.header("🎯 Daily Goal Tracker")

if "goals" not in st.session_state:
    st.session_state.goals = []

goal = st.text_input("✍ Add today's goal")

if st.button("➕ Add Goal"):
    if goal:
        st.session_state.goals.append({"goal": goal, "done": False})

for i, g in enumerate(st.session_state.goals):
    st.session_state.goals[i]["done"] = st.checkbox(
        f"✅ {g['goal']}", value=g["done"]
    )

# ------------------ PROGRESS ------------------
st.header("📊 Progress Summary")

completed = sum(g["done"] for g in st.session_state.goals)
total = len(st.session_state.goals)

if total > 0:
    st.write(f"Completed: {completed}/{total}")
    st.progress(completed / total)

    st.bar_chart({
        "Completed": [completed],
        "Remaining": [total - completed]
    })
else:
    st.write("No goals added yet")

# ------------------ STUDY TIPS ------------------
st.header("💡 Smart Study Tips")

st.success("""
✔ Study consistently  
✔ Focus on weak areas  
✔ Revise daily  
✔ Practice questions  
✔ Take breaks  
""")
