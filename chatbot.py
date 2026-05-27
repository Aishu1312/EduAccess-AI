def chatbot_response(user_input):

    user_input = user_input.lower()

    if "summary" in user_input:
        return "Open AI Notes Summarizer, paste notes, and click Generate Summary."

    elif "quiz" in user_input:
        return "Go to Quiz Generator and enter exam name and topic."

    elif "speech" in user_input:
        return "Use microphone option in Speech-to-Text section."

    elif "dyslexia" in user_input:
        return "Dyslexia mode improves readability using larger fonts and spacing."

    else:
        return "Welcome to EduAccess AI. How may I assist you?"
