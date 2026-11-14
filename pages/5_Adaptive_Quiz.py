from concurrent.futures import ThreadPoolExecutor

import streamlit as st
from ai import generate_questions
from db import init_quiz_table, save_result

st.set_page_config(page_title="Adaptive Quiz", page_icon="🎯")
from style import apply_style
apply_style()
init_quiz_table()

if "user" not in st.session_state:
    st.warning("Please log in from the home page first.")
    st.stop()

user = st.session_state["user"]
st.title("🎯 Adaptive Quiz")
st.write("Answer correctly and the questions get harder. "
         "Answer wrongly and they get easier.")

LEVELS = ["Easy", "Medium", "Hard"]
TOTAL = 5
ORDER = {
    "Easy": ["Easy", "Medium", "Hard"],
    "Medium": ["Medium", "Easy", "Hard"],
    "Hard": ["Hard", "Medium", "Easy"],
}


def pick_question(pools, level):
    for lv in ORDER[level]:
        if pools[lv]:
            return pools[lv].pop(0), lv
    return None, level


detail = st.session_state.get("detail", "a school or college student")

subject = st.selectbox(
    "Subject",
    ["Maths", "Science", "Physics", "Chemistry", "Biology",
     "English", "Computer Science", "Social Science", "Other"],
)
topic = st.text_input("Topic", placeholder="Example: Photosynthesis")

if st.button("Start adaptive quiz"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        pools = {}
        with st.spinner("Preparing your questions. About 15 seconds..."):
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {
                    lv: executor.submit(generate_questions, subject, topic, detail, lv, 4)
                    for lv in LEVELS
                }
                for lv, fut in futures.items():
                    pools[lv] = fut.result()
        failed = any(not qs for qs in pools.values())

        if failed:
            st.error("Could not prepare the quiz. Please click Start again in a minute.")
        else:
            counter = st.session_state.get("adaptive_counter", 0) + 1
            st.session_state["adaptive_counter"] = counter
            first, first_level = pick_question(pools, "Medium")
            st.session_state["adaptive"] = {
                "id": counter,
                "pools": pools,
                "level": first_level,
                "current": first,
                "asked": [],
                "subject": subject,
                "topic": topic,
                "done": False,
                "feedback": "",
            }

ad = st.session_state.get("adaptive")

# ---------- Quiz in progress ----------
if ad and not ad["done"]:
    n = len(ad["asked"]) + 1
    q = ad["current"]

    st.progress((n - 1) / TOTAL)
    st.subheader(f"Question {n} of {TOTAL}  |  Difficulty: {ad['level']}")

    if ad["feedback"]:
        st.info(ad["feedback"])

    choice = st.radio(q["question"], q["options"], index=None,
                      key=f"ad_{ad['id']}_{n}")

    if st.button("Submit answer", key=f"submit_{ad['id']}_{n}"):
        if choice is None:
            st.warning("Please choose an answer first.")
        else:
            correct = choice == q["answer"]
            ad["asked"].append({
                "question": q["question"],
                "chosen": choice,
                "answer": q["answer"],
                "level": ad["level"],
                "correct": correct,
                "explanation": q.get("explanation", ""),
            })

            idx = LEVELS.index(ad["level"])
            new_idx = min(idx + 1, 2) if correct else max(idx - 1, 0)
            new_level = LEVELS[new_idx]

            if len(ad["asked"]) >= TOTAL:
                ad["done"] = True
            else:
                nxt, used = pick_question(ad["pools"], new_level)
                if nxt is None:
                    ad["done"] = True
                else:
                    ad["current"] = nxt
                    ad["level"] = used
                    if correct:
                        result_text = "✅ Correct!"
                    else:
                        result_text = f"❌ Wrong. Correct answer: {q['answer']}."
                    ad["feedback"] = (f"{result_text} {q.get('explanation', '')} "
                                      f"Next question difficulty: {used}")

            if ad["done"]:
                score = sum(1 for a in ad["asked"] if a["correct"])
                save_result(user["id"], ad["subject"], ad["topic"],
                            "Adaptive", score, len(ad["asked"]))
            st.rerun()

# ---------- Quiz finished ----------
if ad and ad["done"]:
    asked = ad["asked"]
    total = len(asked)
    score = sum(1 for a in asked if a["correct"])

    st.metric("Your score", f"{score} / {total}")
    st.write("**Difficulty path:** " + " → ".join(a["level"] for a in asked))

    if score == total:
        st.success("Perfect! 🎉")
    elif score >= total / 2:
        st.info("Good job! Review the ones you missed.")
    else:
        st.warning("Keep practising. Read the explanations below.")

    for i, a in enumerate(asked):
        if a["correct"]:
            st.success(f"Q{i + 1} ({a['level']}). {a['question']}  \n"
                       f"✅ Your answer: {a['chosen']}")
        else:
            st.error(f"Q{i + 1} ({a['level']}). {a['question']}  \n"
                     f"❌ Your answer: {a['chosen']}  \n"
                     f"✔️ Correct answer: {a['answer']}")
        st.caption(f"💡 {a['explanation']}")