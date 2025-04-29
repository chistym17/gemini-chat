from utils import (
    get_gemini_api_key,
    setup_gemini,
    save_feedback,
    log_chat,
    validate_rating,
    FEEDBACK_FILE,
    CHAT_HISTORY_FILE,
    SYSTEM_PROMPT,
    parse_llm_response
)


def main():
    print("Welcome to the Gemini CLI Chatbot!")
    api_key = get_gemini_api_key()
    model = setup_gemini(api_key)
    chat_history = []
    system_prompt = SYSTEM_PROMPT
    exit_handled = False
    
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        log_chat("You", user_input, chat_file=CHAT_HISTORY_FILE)
        chat_history.append({"role": "user", "parts": [user_input]})

        prompt = system_prompt + "\n" + "\n".join([
            f"User: {entry['parts'][0]}" if entry['role'] == 'user' else f"Gemini: {entry['parts'][0]}" for entry in chat_history
        ])
        try:
            response = model.generate_content(prompt)
            llm_output = response.text.strip()
            result = parse_llm_response(llm_output)
        except Exception as e:
            print(f"Gemini: [Error: {e}]")
            log_chat("Gemini", f"[Error: {e}]", chat_file=CHAT_HISTORY_FILE)
            continue

        print(f"Gemini: {result.get('response', '')}")
        log_chat("Gemini", result.get('response', ''), chat_file=CHAT_HISTORY_FILE)

        if result.get("exit_intent"):
            review = result.get("review")
            rating = result.get("rating")
            if review and rating and validate_rating(str(rating)):
                save_feedback(review, rating, feedback_file=FEEDBACK_FILE)
                log_chat("Gemini", "Thank you for your feedback!", chat_file=CHAT_HISTORY_FILE)
                break
            else:
                while True:
                    feedback_input = input("You (feedback): ").strip()
                    log_chat("You", feedback_input, chat_file=CHAT_HISTORY_FILE)
                    chat_history.append({"role": "user", "parts": [feedback_input]})
                    prompt = system_prompt + "\n" + "\n".join([
                        f"User: {entry['parts'][0]}" if entry['role'] == 'user' else f"Gemini: {entry['parts'][0]}" for entry in chat_history
                    ])
                    try:
                        response = model.generate_content(prompt)
                        llm_output = response.text.strip()
                        result = parse_llm_response(llm_output)
                    except Exception as e:
                        print(f"Gemini: [Error: {e}]")
                        log_chat("Gemini", f"[Error: {e}]", chat_file=CHAT_HISTORY_FILE)
                        continue
                    print(f"Gemini: {result.get('response', '')}")
                    log_chat("Gemini", result.get('response', ''), chat_file=CHAT_HISTORY_FILE)
                    review = result.get("review")
                    rating = result.get("rating")
                    if review and rating and validate_rating(str(rating)):
                        save_feedback(review, rating, feedback_file=FEEDBACK_FILE)
                        log_chat("Gemini", "Thank you for your feedback!", chat_file=CHAT_HISTORY_FILE)
                        exit_handled = True
                        break
                if exit_handled:
                    break

if __name__ == "__main__":
    main()
