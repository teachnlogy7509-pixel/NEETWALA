import os
import google.generativeai as genai

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


def ask_gemini(prompt: str) -> str:
    keys = [os.getenv("GEMINI_API_KEY_1"), os.getenv("GEMINI_API_KEY_2"), os.getenv("GEMINI_API_KEY")]
    last_error = None
    for key in keys:
        if not key:
            continue
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as error:
            last_error = error
    if last_error:
        return "Gemini API error: " + str(last_error)
    return "Gemini API key configured नहीं है।"


def translate_text(text: str, target_language: str) -> str:
    return ask_gemini(f"""
    नीचे दिए गए text को {target_language} में translate करो।
    Meaning, scientific terms, headings और formatting को preserve करो।
    कोई नया fact मत जोड़ो। केवल translation दो।

    TEXT:
    {text}
    """)


def generate_pdf_knowledge(text: str, chapter: str) -> str:
    return ask_gemini(f"""
    तुम NEET Biology knowledge bot हो। नीचे PDF से निकला text है।
    Chapter: {chapter}
    केवल Hindi में concise study notes बनाओ:
    1. मुख्य concept
    2. NCERT key points
    3. Important terms
    4. 5 छोटे revision questions और उनके answers
    Text से बाहर की जानकारी मत गढ़ो।

    PDF TEXT:
    {text}
    """)
