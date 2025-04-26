import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

EXIT_KEYWORDS = ["bye", "exit", "end chat", "i want to leave"]

FEEDBACK_FILE = "feedback.txt"
CHAT_HISTORY_FILE = "chat_history.txt"
MODEL_NAME = "models/gemini-2.0-flash"



def get_gemini_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        key = input("Enter your Gemini API key: ").strip()
    return key


def setup_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    return model


def is_exit_intent(text):
    return any(k in text.lower() for k in EXIT_KEYWORDS)


def save_feedback(review, rating, feedback_file=FEEDBACK_FILE):
    with open(feedback_file, "a") as f:
        f.write(f"Review: {review}\nRating: {rating}\n{'-'*30}\n")


def log_chat(user, message, chat_file=CHAT_HISTORY_FILE):
    with open(chat_file, "a") as f:
        f.write(f"{user}: {message}\n")


def validate_rating(rating):
    try:
        val = int(rating)
        return 1 <= val <= 5
    except Exception:
        return False
