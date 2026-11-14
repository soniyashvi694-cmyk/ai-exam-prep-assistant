import streamlit as st
from db import init_db, register_user, login_user

st.set_page_config(page_title="AI Exam Prep Assistant", page_icon="📚")
from style import apply_style
apply_style()
init_db()

st.title("📚 AI Exam Preparation Assistant")

# ---------- Not logged in: show Login / Register ----------
if "user" not in st.session_state:
    st.write("Please log in or create an account to continue.")
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state["user"] = user
                st.rerun()
            else:
                st.error("Wrong username or password.")

    with tab_register:
        new_username = st.text_input("Choose a username", key="reg_username")
        new_password = st.text_input("Choose a password (min 6 characters)",
                                     type="password", key="reg_password")
        if st.button("Create account"):
            ok, message = register_user(new_username, new_password)
            if ok:
                st.success(message + " Now open the Login tab and log in.")
            else:
                st.error(message)

    st.stop()

# ---------- Logged in ----------
user = st.session_state["user"]
st.sidebar.write(f"Logged in as **{user['username']}**")
if st.sidebar.button("Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.success(f"Welcome, {user['username']}! Fill in your details, then open a page from the sidebar.")

level = st.selectbox("Select your level",
                     ["School (Class 5-12)", "College (B.Tech / BCA)", "Competitive Exam"])

if level == "School (Class 5-12)":
    class_list = ["Class 5", "Class 6", "Class 7", "Class 8",
                  "Class 9", "Class 10", "Class 11", "Class 12"]
    student_class = st.selectbox("Select your class", class_list)
    if student_class in ["Class 11", "Class 12"]:
        stream = st.selectbox("Select your stream", ["Science", "Commerce", "Arts"])
        detail = f"{student_class} ({stream})"
    else:
        detail = student_class
elif level == "College (B.Tech / BCA)":
    semester = st.selectbox("Select your semester",
                            [f"Semester {i}" for i in range(1, 9)])
    detail = f"B.Tech/BCA {semester}"
else:
    detail = st.selectbox("Select exam", ["JEE", "NEET", "GATE", "CUET", "Other"])

exam_type = st.selectbox("Which exam are you preparing for?",
                         ["Unit Test", "Mid-term", "Half-yearly", "Final / Annual Exam"])

st.session_state["detail"] = detail
st.session_state["exam_type"] = exam_type
st.info(f"Profile: {detail}, {exam_type}. Open **Study Plan** from the sidebar.")