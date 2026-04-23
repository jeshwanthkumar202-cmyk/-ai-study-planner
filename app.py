import streamlit as st
from datetime import date

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Study Planner", layout="wide")

# ------------------ FULL UI FIX ------------------
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color: #ffffff;
}

/* FORCE MAIN TEXT DARK */
.main, .block-container {
    color: #111827 !important;
}

/* HEADINGS */
h1, h2, h3, h4, h5 {
    color: #111827 !important;
    font-weight: 700;
}

/* ALL TEXT FIX */
p, span, label, div {
    color: #111827 !important;
    font-size: 18px !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #0f172a !important;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
    font-size: 16px !important;
}

/* SIDEBAR INPUT BOXES */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border-radius: 8px;
}

/* BUTTON STYLE */
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
    border-radius: 10px;
    height: 45px;
    width: 230px;
    font-size: 18px;
}

/* INPUT BOXES MAIN */
input, textarea {
    color: #111827 !important;
    font-size: 16px !important;
}

/* PROGRESS BAR */
.stProgress > div > div {
    background-color: #2563eb;
}

</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("📚 AI Personalized Study Planner")

# ------------------ SIDEBAR ------------------
st.sidebar.header("📥 Enter Details")

subjects = st.sidebar.text_input("📘 Subjects (comma separated)")
hours = st.sidebar.slider("⏱ Study hours/day", 1, 12, 4)
exam_date = st.sidebar.date_input("📅 Exam Date", min_value=date.today())
weak_areas = st.sidebar.text_area("⚠ Weak Areas")

# ------------------ GENERATE PLAN ------------------
if st.sidebar.button("🚀 Generate Plan"):

    if subjects.strip() == "":
        st.warning("⚠ Please enter subjects")
    else:
        subject_list = [s.strip() for s in subjects.split(",") if s.strip()]
        days_left = (exam_date - date.today()).days

        if days_left <= 0:
            st.error("❌ Exam date must be in the future")
        else:
            st.subheader("📅 Your Study Plan")

            plan_text = ""
            per_time = max(1, hours // len(subject_list))

            for day in range(1, days_left + 1):
                st.markdown(f"### 📆 Day {day}")
                plan_text += f"Day {day}\n"

                for sub in subject_list:
                    line = f"📘 {sub} → {per_time} hrs"
                    st.write(line)
                    plan_text += line + "\n"

                plan_text += "\n"

            # Weak areas
            if weak_areas:
                st.subheader("⚠ Focus More On")
                st.write(weak_areas)
                plan_text += f"\nFocus Areas: {weak_areas}\n"

            st.success("✅ Plan Generated Successfully!")

            # DOWNLOAD
            st.download_button(
                label="📥 Download Plan",
                data=plan_text,
                file_name="study_plan.txt",
                mime="text/plain"
            )

# ------------------ PROGRESS TRACKER ------------------
st.header("📈 Progress Tracker")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

new_task = st.text_input("✍ Add Completed Topic")

if st.button("➕ Add Progress"):
    if new_task:
        st.session_state.tasks.append({"task": new_task, "done": False})

for i, task in enumerate(st.session_state.tasks):
    st.session_state.tasks[i]["done"] = st.checkbox(
        f"✅ {task['task']}", value=task["done"]
    )

# ------------------ STUDY TIPS ------------------
st.header("💡 Smart Study Tips")

st.success("""
✔ Study in small sessions (Pomodoro: 25 min)  
✔ Revise regularly  
✔ Focus more on weak subjects  
✔ Take proper sleep  
✔ Practice previous papers  
""")

# ------------------ PROGRESS SUMMARY ------------------
st.header("📊 Your Progress Summary")

completed = sum(t["done"] for t in st.session_state.tasks)
total = len(st.session_state.tasks)

if total > 0:
    st.write(f"✅ Completed: {completed}/{total}")
    st.progress(completed / total)
else:
    st.write("No tasks added yet")
