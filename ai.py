import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Tried in order until one works. If errors appear later,
# run list_models.py and update this list.
MODELS = [
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
]

# Remembers the model that answered last, so it is tried first next time
_working = {"model": None}


def ask_ai(prompt):
    order = list(MODELS)
    if _working["model"] in order:
        order.remove(_working["model"])
        order.insert(0, _working["model"])

    for model in order:
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            _working["model"] = model
            return response.text
        except Exception as e:
            print(f"{model} failed: {str(e)[:100]}")
            time.sleep(0.5)
    return "Sorry, the AI is busy right now. Please try again in a minute."


def generate_questions(subject, topic, level, difficulty, count=5):
    import json

    prompt = f"""
You are an exam question writer.
Create {count} multiple-choice questions.
Subject: {subject}
Topic: {topic}
Student level: {level}
Difficulty: {difficulty}

Return ONLY a JSON list. No extra text and no markdown fences.
Each item must look exactly like this:
{{"question": "...", "options": ["option 1", "option 2", "option 3", "option 4"], "answer": "the exact text of the correct option", "explanation": "one short sentence"}}

Rules:
- Exactly 4 options per question and only one correct option.
- The answer must be copied exactly from the options.
- Questions must match the student's level and the difficulty.
"""
    text = ask_ai(prompt)
    if text.startswith("Sorry"):
        return None

    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        return None

    try:
        data = json.loads(text[start:end + 1])
    except Exception:
        return None

    good = []
    for q in data:
        try:
            if len(q["options"]) == 4 and q["answer"] in q["options"]:
                good.append(q)
        except Exception:
            continue

    return good if good else None