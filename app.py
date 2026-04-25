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
st.set_page_config(
    page_title="AI Study Planner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ FORCE LIGHT THEME ------------------
st.markdown("""
<style>

/* GLOBAL */
html, body, [class*="css"] {
    background-color: #f9fafb !important;
    color: #111827 !important;
    font-size: 18px !important;
}

/* HEADINGS */
h1, h2, h3 {
    color: #111827 !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #1e293b);
}
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* INPUTS */
input, textarea {
    color: #111827 !important;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    color: white;
    border-radius: 12px;
    height: 45px;
    font-size: 18px;
}

/* CARD STYLE */
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("📚 AI Personalized Study Planner")

# ------------------ SIDEBAR ------------------
st.sidebar.header("📥 Enter Details")

subjects = st.sidebar.text_input("📘 Subjects")
hours = st.sidebar.slider("⏱ Study hours/day", 1, 12, 4)
exam_date = st.sidebar.date_input("📅 Exam Date", min_value=date.today())
weak_areas = st.sidebar.text_area("⚠ Weak Areas")

# ------------------ AI FUNCTION ------------------
def generate_plan(subjects, hours, days, weak):
    if client:
        prompt = f"""
        Create a structured study plan.

        Subjects: {subjects}
        Hours/day: {hours}
        Days: {days}
        Weak areas: {weak}

        Keep it simple and clear.
        """
        try:
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return res.choices[0].message.content
        except:
            return "⚠ AI error. Showing basic plan instead."

    # fallback (no AI)
    subject_list = [s.strip() for s in subjects.split(",")]
    plan = ""
    per = max(1, hours // len(subject_list))

    for d in range(1, days+1):
        plan += f"Day {d}\n"
        for s in subject_list:
            plan += f"- {s}: {per} hrs\n"
        plan += "\n"

    return plan

# ------------------ GENERATE ------------------
if st.sidebar.button("🚀 Generate Plan"):
    if not subjects:
        st.warning("Enter subjects")
    else:
        days = (exam_date - date.today()).days

        if days <= 0:
            st.error("Invalid exam date")
        else:
            with st.spinner("Generating..."):
                plan = generate_plan(subjects, hours, days, weak_areas)

            # CARD DISPLAY
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📅 Study Plan")
            st.write(plan)
            st.markdown('</div>', unsafe_allow_html=True)

            st.download_button("📥 Download Plan", plan)

# ------------------ PROGRESS TRACKER ------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📈 Progress Tracker")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

task = st.text_input("Add completed topic")

if st.button("➕ Add"):
    if task:
        st.session_state.tasks.append({"task": task, "done": False})

for i, t in enumerate(st.session_state.tasks):
    st.session_state.tasks[i]["done"] = st.checkbox(t["task"], value=t["done"])

done = sum(t["done"] for t in st.session_state.tasks)
total = len(st.session_state.tasks)

if total:
    st.progress(done / total)
    st.write(f"{done}/{total} completed")
else:
    st.write("No tasks yet")

st.markdown('</div>', unsafe_allow_html=True)

# ------------------ METRICS ------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Quick Stats")

col1, col2, col3 = st.columns(3)
col1.metric("Subjects", len(subjects.split(",")) if subjects else 0)
col2.metric("Hours/Day", hours)
col3.metric("Days Left", (exam_date - date.today()).days)

st.markdown('</div>', unsafe_allow_html=True)

# ------------------ TIPS ------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💡 Smart Tips")

st.success("""
✔ Study consistently  
✔ Focus weak areas  
✔ Revise regularly  
✔ Take breaks  
✔ Sleep well  
""")

st.markdown('</div>', unsafe_allow_html=True)
