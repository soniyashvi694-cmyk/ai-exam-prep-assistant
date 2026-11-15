# AI-Based Exam Preparation Assistant

   **Live app:** https://yashvi-exam-prep.streamlit.app

A web app that helps school and college students prepare for exams.
Built with Python, Streamlit, SQLite and the Google Gemini API.

## Features
1. User registration and login (passwords stored as salted hashes)
2. AI study plan generator (based on subjects, exam date and daily hours)
3. AI question generator (MCQs with explanations)
4. Adaptive quiz (difficulty changes with your answers)
5. AI doubt-solving chatbot
6. Performance dashboard (accuracy trends, weak and strong topics)

## How to run
1. Install Python 3.10 or newer.
2. Create a virtual environment:   python -m venv venv
3. Activate it:                    venv\Scripts\activate
4. Install packages:               pip install -r requirements.txt
5. Create a file named .env and add your key:   GEMINI_API_KEY=your_key_here
6. Start the app:                  streamlit run app.py

## Project structure
- app.py            home page, login and register
- pages/            Study Plan, My Plans, Doubt Solver, Quiz, Adaptive Quiz, Dashboard
- ai.py             all calls to the Gemini API
- db.py             SQLite database functions
- style.py          colours and styling

## Student
Yashvi Soni, B.Tech (AI/ML), Career Point University
Project Guide: Mr. Harsh Verma