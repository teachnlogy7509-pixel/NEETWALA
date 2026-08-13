import os
from google import genai

API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
]

# नए SDK के लिए मॉडल का नाम बिना 'models/' के होना चाहिए
MODEL = "gemini-1.5-flash"

def ask_gemini(prompt: str) -> str:
    last_error = None

    for key in API_KEYS:
        if not key:
            continue

        try:
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )

            if response and response.text:
                return response.text

        except Exception as e:
            last_error = e
            continue

    return f"Gemini API Error: {last_error}"
