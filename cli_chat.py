from utils import (
    get_gemini_api_key,
    setup_gemini,
    is_exit_intent,
    save_feedback,
    log_chat,
    validate_rating,
    FEEDBACK_FILE,
    CHAT_HISTORY_FILE 
)




def main():
    print("Welcome to the Gemini CLI Chatbot!")
    api_key = get_gemini_api_key()
    model = setup_gemini(api_key)
    chat_history = []
    while True:

        user_input = input("You: ").strip()
        if not user_input:
            continue
        log_chat("You", user_input, chat_file=CHAT_HISTORY_FILE)
        chat_history.append({"role": "user", "parts": [user_input]})

        if is_exit_intent(user_input):
            print("Gemini: Before you go, could you leave a short review and rate your experience (1-5)?")
            review = input("Review: ").strip()
            rating = input("Rating (1-5): ").strip()
            while not validate_rating(rating):
                print("Please enter a valid rating (1-5).")
                rating = input("Rating (1-5): ").strip()
            save_feedback(review, rating, feedback_file=FEEDBACK_FILE)
            print("Gemini: Thank you for your feedback!")
            log_chat("Gemini", "Thank you for your feedback!", chat_file=CHAT_HISTORY_FILE)
            break

        try:
            response = model.generate_content(user_input)
            answer = response.text.strip()
        except Exception as e:
            answer = f"[Error: {e}]"
        print(f"Gemini: {answer}")
        log_chat("Gemini", answer, chat_file=CHAT_HISTORY_FILE)

if __name__ == "__main__":
    main()
