import streamlit as st


def apply_style():
    st.markdown(
        """
        <style>
        /* Background */
        .stApp {
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 45%, #0f172a 100%);
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.9);
            border-right: 1px solid rgba(251, 191, 36, 0.3);
        }

        /* Titles */
        h1 {
            color: #fde68a !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
        }
        h2, h3 {
            color: #fcd34d !important;
        }

        /* Buttons */
        .stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
            background: linear-gradient(90deg, #f59e0b, #ef4444);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.5rem 1.2rem;
            font-weight: 600;
            transition: transform 0.15s;
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover,
        .stDownloadButton > button:hover {
            transform: scale(1.05);
            color: white;
        }

        /* Cards */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 14px;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }
        [data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.06);
            border-radius: 12px;
        }

        /* Floating stickers on the right side */
        .stickers {
            position: fixed;
            right: 18px;
            top: 30%;
            display: flex;
            flex-direction: column;
            gap: 18px;
            font-size: 2.2rem;
            opacity: 0.55;
            pointer-events: none;
            z-index: 0;
        }
        </style>

        <div class="stickers">
            <span>📚</span>
            <span>✏️</span>
            <span>🎓</span>
            <span>💡</span>
            <span>🚀</span>
        </div>
        """,
        unsafe_allow_html=True,
    )