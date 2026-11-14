import streamlit as st
from db import get_plans

st.set_page_config(page_title="My Plans", page_icon="📂")
from style import apply_style
apply_style()

if "user" not in st.session_state:
    st.warning("Please log in from the home page first.")
    st.stop()

user = st.session_state["user"]
st.title("📂 My Saved Plans")

plans = get_plans(user["id"])

if not plans:
    st.info("You have no saved plans yet. Generate one on the Study Plan page and click Save.")

for plan_id, title, content, created_at in plans:
    with st.expander(f"{title}  ({created_at[:10]})"):
        st.markdown(content)