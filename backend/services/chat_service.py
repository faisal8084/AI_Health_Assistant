from src.chatbot.chatbot_engine import ChatbotEngine


# Store chatbot instances for different sessions
sessions = {}


def process_chat(session_id: str, message: str):

    # Create new chatbot for new session
    if session_id not in sessions:

        sessions[session_id] = ChatbotEngine()

    # Get existing chatbot
    chatbot = sessions[session_id]

    # Process user message
    result = chatbot.process_message(message)

    return result

   #Chat reset karne ke liye
def reset_chat(session_id: str):

    if session_id in sessions:

        sessions[session_id] = ChatbotEngine()

        return {
            "success": True,
            "message": "Conversation reset successfully."
        }

    return {
        "success": False,
        "message": "Session not found."
    }