import pandas as pd
import streamlit as st
from ai import ask_ai
from db import init_quiz_table, get_results

st.set_page_config(page_title="Dashboard", page_icon="📊")
from style import apply_style
apply_style()
init_quiz_table()

if "user" not in st.session_state:
    st.warning("Please log in from the home page first.")
    st.stop()

user = st.session_state["user"]
st.title("📊 Performance Dashboard")

rows = get_results(user["id"])

if not rows:
    st.info("No quiz results yet. Take a quiz on the Quiz or Adaptive Quiz page, "
            "then come back here.")
    st.stop()

# ---------- Prepare the data ----------
df = pd.DataFrame(rows, columns=["Subject", "Topic", "Difficulty", "Score", "Total", "Date"])
df["Accuracy"] = (df["Score"] / df["Total"] * 100).round(0)
df["Topic"] = df["Topic"].str.strip().str.title()
df = df.iloc[::-1].reset_index(drop=True)      # oldest first
df["Attempt"] = df.index + 1

# ---------- Big numbers ----------
total_correct = int(df["Score"].sum())
total_questions = int(df["Total"].sum())
overall = round(total_correct / total_questions * 100) if total_questions else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Quizzes taken", len(df))
c2.metric("Questions answered", total_questions)
c3.metric("Overall accuracy", f"{overall}%")
c4.metric("Best score", f"{int(df['Accuracy'].max())}%")

# ---------- Progress over time ----------
st.subheader("📈 Accuracy over time")
st.line_chart(df.set_index("Attempt")["Accuracy"])

# ---------- Accuracy by topic ----------
topic_stats = df.groupby("Topic")[["Score", "Total"]].sum()
topic_stats["Accuracy"] = (topic_stats["Score"] / topic_stats["Total"] * 100).round(0)

st.subheader("📚 Accuracy by topic")
st.bar_chart(topic_stats["Accuracy"])

# ---------- Strong and weak topics ----------
weak = topic_stats[topic_stats["Accuracy"] < 50]
strong = topic_stats[topic_stats["Accuracy"] >= 80]

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("⚠️ Weak topics")
    if weak.empty:
        st.success("No weak topics. Great work!")
    else:
        for topic, row in weak.sort_values("Accuracy").iterrows():
            st.error(f"{topic}: {int(row['Accuracy'])}%")
with col_b:
    st.subheader("💪 Strong topics")
    if strong.empty:
        st.info("Keep practising to build strong topics.")
    else:
        for topic, row in strong.sort_values("Accuracy", ascending=False).iterrows():
            st.success(f"{topic}: {int(row['Accuracy'])}%")

# ---------- AI revision advice ----------
if not weak.empty:
    if st.button("🤖 Get AI revision tips for my weak topics"):
        weak_list = ", ".join(weak.index)
        detail = st.session_state.get("detail", "a school or college student")
        prompt = f"""
You are a friendly tutor. The student ({detail}) scored below 50% in these topics: {weak_list}.
Give a short revision plan: for each topic, 2 quick tips and one practice idea.
Keep it under 200 words and use simple language.
"""
        with st.spinner("Thinking..."):
            advice = ask_ai(prompt)
        st.markdown(advice)

# ---------- Recent attempts ----------
st.subheader("🕒 Recent attempts")
recent = df.iloc[::-1].copy()
recent["Score"] = recent["Score"].astype(str) + " / " + recent["Total"].astype(str)
recent["Date"] = recent["Date"].astype(str).str[:16]
recent["Accuracy"] = recent["Accuracy"].astype(int).astype(str) + "%"
st.dataframe(
    recent[["Date", "Subject", "Topic", "Difficulty", "Score", "Accuracy"]],
    use_container_width=True,
    hide_index=True,
)