import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()


FEEDBACK_FILE = "feedback.txt"
CHAT_HISTORY_FILE = "chat_history.txt"
MODEL_NAME = "models/gemini-2.0-flash"

SYSTEM_PROMPT = """
You are a helpful chatbot assistant in a CLI chat app. Your responsibilities:
- Always reply in a friendly and helpful manner.
- Detect if the user intends to end the conversation, not just by keywords but by understanding the user's intent/context (e.g., 'thank you', 'that's all', 'goodbye', etc.).
- If you detect the user wants to end the conversation, try to extract a review and a rating (1-5) from their message if present.
- If the review and/or rating are not provided in the user's message, politely ask the user to provide both in any format they like.
- When you reply, always return a JSON object with the following fields:
  - exit_intent: true or false (whether the user wants to end the conversation)
  - review: string or null (the user's review if provided)
  - rating: integer 1-5 or null (the user's rating if provided)
  - response: string (your reply to the user)
- Never fabricate a review or rating if the user hasn't given one. Always ask again if missing.
- Example JSON: {"exit_intent": true, "review": "Great service!", "rating": 5, "response": "Thank you for your feedback!"}
"""

import json

def get_gemini_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        key = input("Enter your Gemini API key: ").strip()
    return key


def setup_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    return model


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


def parse_llm_response(text):
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start == -1 or end == -1:
            raise ValueError("No JSON object found.")
        json_str = text[start:end]
        data = json.loads(json_str)
        return data
    except Exception as e:
        return {"exit_intent": False, "review": None, "rating": None, "response": f"[Parsing error: {e}"}
