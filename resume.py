
quiz_state = {}

def save_progress(user_id, topic, current_question):
    quiz_state[user_id] = {
        "topic": topic,
        "current_question": current_question,
    }

def load_progress(user_id):
    return quiz_state.get(user_id)
