# Gemini CLI Chat Application

## Setup Instructions

1. **Clone the repository or download the project files**
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Obtain a Gemini API key:**
   - Register for a free API key here: https://makersuite.google.com/app/apikey
   - Save your API key securely (you will be prompted to enter it on first run, or you can set it as an environment variable `GEMINI_API_KEY`).

## How to Run the Application

```bash
python cli_chat.py
```

## Example Chat Session
```
You: Hi!
Gemini: Hello! How can I help you today?
You: Tell me a joke.
Gemini: Why did the computer go to the doctor? Because it had a virus!
You: bye
Gemini: Before you go, could you please leave a short review and rate your experience (1-5)?
You: Sure! It was great. 5
Gemini: Thank you for your feedback!
```

## Gemini API Setup Guide
- Get your free API key: https://makersuite.google.com/app/apikey

## Notes
- Reviews and ratings are saved in `feedback.txt`.
- All chat conversations are logged in `chat_history.txt`.
- Handles exit prompts like "bye", "exit", "end chat", etc.
