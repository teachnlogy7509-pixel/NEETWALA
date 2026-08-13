
from bot.services.gemini import ask_gemini

def generate_neet_quiz(topic: str, count: int = 90):
    count = max(10, min(180, count))
    prompt = f"""
    केवल हिंदी में {count} मूल NEET-स्तर के जीवविज्ञान MCQ बनाओ।
    विषय: {topic}
    नियम:
    - 4 विकल्प
    - सही उत्तर
    - संक्षिप्त व्याख्या
    - NCERT आधारित
    - Assertion-Reason प्रश्न भी शामिल करो
    """
    return ask_gemini(prompt)
