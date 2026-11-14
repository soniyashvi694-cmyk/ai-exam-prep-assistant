import streamlit as st
from ai import generate_questions
from db import init_quiz_table, save_result

st.set_page_config(page_title="Quiz", page_icon="📝")
from style import apply_style
apply_style()
init_quiz_table()

if "user" not in st.session_state:
    st.warning("Please log in from the home page first.")
    st.stop()

user = st.session_state["user"]
st.title("📝 AI Quiz")

detail = st.session_state.get("detail", "a school or college student")

subject = st.selectbox(
    "Subject",
    ["Maths", "Science", "Physics", "Chemistry", "Biology",
     "English", "Computer Science", "Social Science", "Other"],
)
topic = st.text_input("Topic", placeholder="Example: Photosynthesis")
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=1)
count = st.slider("Number of questions", 3, 10, 5)

if st.button("Generate quiz"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Creating your questions..."):
            questions = generate_questions(subject, topic, detail, difficulty, count)
        if questions:
            counter = st.session_state.get("quiz_counter", 0) + 1
            st.session_state["quiz_counter"] = counter
            st.session_state["quiz"] = {
                "id": counter,
                "questions": questions,
                "subject": subject,
                "topic": topic,
                "difficulty": difficulty,
                "submitted": False,
            }
        else:
            st.error("Could not create the quiz. Please click Generate quiz again.")

quiz = st.session_state.get("quiz")

if quiz:
    questions = quiz["questions"]
    st.subheader(f"{quiz['topic']} ({quiz['difficulty']})")

    if not quiz["submitted"]:
        with st.form(f"quiz_form_{quiz['id']}"):
            answers = []
            for i, q in enumerate(questions):
                choice = st.radio(
                    f"Q{i + 1}. {q['question']}",
                    q["options"],
                    index=None,
                    key=f"q_{quiz['id']}_{i}",
                )
                answers.append(choice)
            submitted = st.form_submit_button("Submit quiz")

        if submitted:
            score = 0
            for a, q in zip(answers, questions):
                if a == q["answer"]:
                    score += 1
            quiz["answers"] = answers
            quiz["score"] = score
            quiz["submitted"] = True
            save_result(user["id"], quiz["subject"], quiz["topic"],
                        quiz["difficulty"], score, len(questions))
            st.rerun()

    else:
        score = quiz["score"]
        total = len(questions)
        st.metric("Your score", f"{score} / {total}")
        if score == total:
            st.success("Perfect score! 🎉")
        elif score >= total / 2:
            st.info("Good job! Review the ones you missed.")
        else:
            st.warning("Keep practising. Read the explanations below.")

        for i, (q, a) in enumerate(zip(questions, quiz["answers"])):
            if a == q["answer"]:
                st.success(f"Q{i + 1}. {q['question']}  \n✅ Your answer: {a}")
            else:
                your = a if a else "(not answered)"
                st.error(f"Q{i + 1}. {q['question']}  \n❌ Your answer: {your}  \n"
                         f"✔️ Correct answer: {q['answer']}")
            st.caption(f"💡 {q['explanation']}")
        