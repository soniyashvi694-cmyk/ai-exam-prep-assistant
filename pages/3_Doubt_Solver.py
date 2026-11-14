import streamlit as st
from ai import ask_ai

st.set_page_config(page_title="Doubt Solver", page_icon="💬")
from style import apply_style
apply_style()

if "user" not in st.session_state:
    st.warning("Please log in from the home page first.")
    st.stop()

st.title("💬 AI Doubt Solver")

detail = st.session_state.get("detail", "a school or college student")

subject = st.selectbox(
    "Subject",
    ["General", "Maths", "Science", "Physics", "Chemistry", "Biology",
     "English", "Computer Science", "Social Science", "Other"],
)

# Keep the conversation in memory
if "chat" not in st.session_state:
    st.session_state["chat"] = []

if st.sidebar.button("🗑️ Clear chat", key="clear_chat"):
    st.session_state["chat"] = []
    st.rerun()

# Show earlier messages
for msg in st.session_state["chat"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box at the bottom
question = st.chat_input("Ask your doubt here...")

if question:
    # Show and store the student's message
    st.session_state["chat"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Build the history text from the last few messages
    history = ""
    for msg in st.session_state["chat"][-7:-1]:
        speaker = "Student" if msg["role"] == "user" else "Tutor"
        history += f"{speaker}: {msg['content']}\n"

    prompt = f"""
You are a friendly, patient tutor helping a student.
Student level: {detail}
Subject: {subject}

Rules:
- Explain in simple language suited to the student's level.
- Use a short real-life example when it helps.
- For maths or science problems, show the steps one by one.
- Keep the answer under 200 words unless the student asks for more.
- If the question is not about studies, politely bring the student back to studying.

Earlier conversation:
{history if history else "(none)"}

Student's new question: {question}
"""

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_ai(prompt)
        st.markdown(answer)

    st.session_state["chat"].append({"role": "assistant", "content": answer})