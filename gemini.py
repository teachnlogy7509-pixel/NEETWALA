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


def generate_short_notes(source: str, title: str = "") -> str:
    return ask_gemini(f"""
    तुम NEET Biology के expert short-notes teacher हो।
    Topic/title: {title or 'NEET Biology'}

    नीचे दिए गए topic या source material से exam-ready, concise Hindi short notes बनाओ।
    अगर source केवल topic का नाम है, तो NCERT-aligned knowledge से notes बनाओ।
    अगर source material दिया गया है, तो उसी की जानकारी को प्राथमिकता दो और facts मत गढ़ो।

    Format exactly इसी तरह रखो:
    1. एक clear title
    2. Concept in 2-3 lines
    3. Important definitions
    4. Key points in bullets
    5. Comparisons/table केवल जहां जरूरी हो
    6. Formula, process या steps जहां लागू हों
    7. NEET exam में याद रखने वाले points
    8. एक mnemonic/trick अगर उपयोगी हो

    Rules:
    - केवल सरल Hindi, जरूरी scientific terms English brackets में
    - बहुत छोटा लेकिन complete; लगभग 500-700 words से अधिक नहीं
    - अनावश्यक introduction, greetings या questions मत लिखो
    - MCQ मत बनाओ; यह केवल short notes हैं

    SOURCE:
    {source[:16000]}
    """)


def generate_pdf_knowledge(text: str, chapter: str) -> str:
    return generate_short_notes(text, chapter)
