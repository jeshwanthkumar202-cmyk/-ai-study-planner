import streamlit as st
from datetime import date

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Study Planner", layout="wide")

# ------------------ FIXED STYLE ------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background-color: #ffffff;
}

h1, h2, h3, h4 {
    color: #000000 !important;
}

p, label, span, div {
    color: #000000 !important;
    font-size: 16px;
}

.stButton>button {
    background-color: #007BFF;
    color: white;
    border-radius: 10px;
    height: 40px;
    width: 220px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("📚 AI Personalized Study Planner")

# ------------------ SIDEBAR INPUT ------------------
st.sidebar.header("📥 Enter Details")

subjects = st.sidebar.text_input("Subjects (comma separated)")
hours = st.sidebar.slider("Study hours/day", 1, 12, 4)
exam_date = st.sidebar.date_input("Exam Date", min_value=date.today())
weak_areas = st.sidebar.text_area("Weak Areas")

# ------------------ MAIN ------------------
if st.sidebar.button("Generate Plan"):

    if subjects.strip() == "":
        st.warning("Please enter subjects")
    else:
        subject_list = [s.strip() for s in subjects.split(",") if s.strip()]
        days_left = (exam_date - date.today()).days

        if days_left <= 0:
            st.error("Exam date must be in the future")
        else:
            st.subheader("📅 Your Study Plan")

            plan_text = ""
            per_time = max(1, hours // len(subject_list))

            for day in range(1, days_left + 1):
                st.markdown(f"### Day {day}")
                plan_text += f"Day {day}\n"

                for sub in subject_list:
                    line = f"- {sub}: {per_time} hrs"
                    st.write(line)
                    plan_text += line + "\n"

                plan_text += "\n"

            # Weak areas highlight
            if weak_areas:
                st.subheader("⚠ Focus More On")
                st.write(weak_areas)
                plan_text += f"\nFocus Areas: {weak_areas}\n"

            st.success("✅ Plan Generated Successfully!")

            # ------------------ DOWNLOAD FEATURE ------------------
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

new_task = st.text_input("Add Topic You Completed")

if st.button("Add Progress"):
    if new_task:
        st.session_state.tasks.append({"task": new_task, "done": False})

for i, task in enumerate(st.session_state.tasks):
    st.session_state.tasks[i]["done"] = st.checkbox(
        task["task"], value=task["done"]
    )

# ------------------ STUDY TIPS ------------------
st.header("💡 Smart Study Tips")

st.info("""
✔ Study in small sessions (Pomodoro: 25 min)  
✔ Revise regularly  
✔ Focus more on weak subjects  
✔ Take proper sleep  
✔ Practice previous papers  
""")

# ------------------ SIMPLE ANALYTICS ------------------
st.header("📊 Your Progress Summary")

completed = sum(t["done"] for t in st.session_state.tasks)
total = len(st.session_state.tasks)

if total > 0:
    st.write(f"✅ Completed: {completed}/{total}")
    st.progress(completed / total)
else:
    st.write("No tasks added yet")
