import streamlit as st
from datetime import date
from ai import ask_ai
from db import save_plan

st.set_page_config(page_title="Study Plan", page_icon="🗓️")
from style import apply_style
apply_style()

if "user" not in st.session_state:
    st.warning("Please log in from the home page first.")
    st.stop()

user = st.session_state["user"]
st.title("🗓️ Study Plan Generator")

detail = st.session_state.get("detail", "Not selected")
exam_type = st.session_state.get("exam_type", "Exam")
st.write(f"Preparing for: **{exam_type}**, **{detail}**")

subjects_text = st.text_input("Subjects (separated by commas)", "Maths, Science")
topics_text = st.text_area("Syllabus / topics (optional)",
                           placeholder="Example: Maths - Algebra, Geometry; Science - Light, Electricity")
exam_date = st.date_input("Exam date", min_value=date.today())
hours = st.slider("Study hours per day", 1, 10, 3)

if st.button("Generate my study plan"):
    days_left = (exam_date - date.today()).days

    if not subjects_text.strip():
        st.warning("Please enter at least one subject.")
    elif days_left < 1:
        st.warning("Please choose an exam date that is at least tomorrow.")
    else:
        prompt = f"""
You are a friendly study planner for a student.
Student level: {detail}
Exam: {exam_type}
Subjects: {subjects_text}
Syllabus / topics: {topics_text if topics_text.strip() else "Use the standard syllabus for this level"}
Days left until the exam: {days_left}
Study hours available per day: {hours}

Create a day-wise study plan as a markdown table with columns:
Day | Subject | Topics to study | Hours.
Rules:
- Balance the subjects and give harder topics more time.
- Reserve the last 2 days for full revision.
- If more than 30 days are left, make a week-wise table instead.
- After the table, add 3 short study tips.
"""
        with st.spinner("Creating your plan..."):
            plan = ask_ai(prompt)

        if plan.startswith("Sorry"):
            st.error(plan)
        else:
            st.session_state["plan"] = plan
            st.session_state["plan_title"] = f"{detail} | {subjects_text} | exam on {exam_date}"

if "plan" in st.session_state:
    st.markdown(st.session_state["plan"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save this plan"):
            save_plan(user["id"], st.session_state["plan_title"], st.session_state["plan"])
            st.success("Plan saved! Find it on the My Plans page.")
    with col2:
        st.download_button("⬇️ Download plan", st.session_state["plan"],
                           file_name="study_plan.md")