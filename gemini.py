import json
import os
import urllib.error
import urllib.request

import google.generativeai as genai

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"


def _content_from_response(payload):
    content = payload.get("choices", [{}])[0].get("message", {}).get("content", "")
    if isinstance(content, list):
        return "".join(item.get("text", "") for item in content if isinstance(item, dict)).strip()
    return str(content).strip()


def _openai_compatible(endpoint, key, model, prompt, extra_headers=None):
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }).encode("utf-8")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    headers.update(extra_headers or {})
    request = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=90) as response:
        data = json.loads(response.read().decode("utf-8"))
    answer = _content_from_response(data)
    if not answer:
        raise RuntimeError("AI provider returned an empty response")
    return answer


def _ask_gemini(prompt):
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
        raise RuntimeError(str(last_error))
    raise RuntimeError("Gemini API key is not configured")


def ask_gemini(prompt: str) -> str:
    """Legacy function name retained; tries OpenRouter, Groq, then Gemini."""
    errors = []
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if openrouter_key:
        try:
            headers = {}
            if os.getenv("OPENROUTER_SITE_URL"):
                headers["HTTP-Referer"] = os.getenv("OPENROUTER_SITE_URL")
            if os.getenv("OPENROUTER_APP_NAME"):
                headers["X-Title"] = os.getenv("OPENROUTER_APP_NAME")
            return _openai_compatible(
                OPENROUTER_ENDPOINT,
                openrouter_key,
                os.getenv("OPENROUTER_MODEL", "openrouter/auto"),
                prompt,
                headers,
            )
        except Exception as error:
            errors.append(f"OpenRouter: {error}")

    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            return _openai_compatible(
                GROQ_ENDPOINT,
                groq_key,
                os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                prompt,
            )
        except Exception as error:
            errors.append(f"Groq: {error}")

    if any(os.getenv(key) for key in ("GEMINI_API_KEY_1", "GEMINI_API_KEY_2", "GEMINI_API_KEY")):
        try:
            return _ask_gemini(prompt)
        except Exception as error:
            errors.append(f"Gemini: {error}")

    return "AI key configured नहीं है। Railway Variables में OPENROUTER_API_KEY, GROQ_API_KEY या GEMINI_API_KEY डालें।" + ("\n" + " | ".join(errors) if errors else "")


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
    Format: clear title, concept, definitions, key bullets, process/formula, NEET points, mnemonic.
    केवल सरल Hindi, जरूरी scientific terms English brackets में। 500-700 words से अधिक नहीं।
    MCQ मत बनाओ; यह केवल short notes हैं।

    SOURCE:
    {source[:16000]}
    """)


def generate_pdf_knowledge(text: str, chapter: str) -> str:
    return generate_short_notes(text, chapter)


def generate_diagram_spec(topic: str) -> dict:
    raw = ask_gemini(f"""
    Create an educational flowchart for this NEET Biology topic: {topic}
    Return ONLY valid JSON, no markdown and no explanation.
    Schema: {{"title":"short title","nodes":[{{"id":"n1","label":"short Hindi label"}}],"edges":[{{"from":"n1","to":"n2","label":"optional"}}]}}
    Use 4 to 9 nodes, simple Hindi labels, and a logical top-to-bottom process.
    """)
    cleaned = raw.strip().replace("```json", "").replace("```", "").strip()
    try:
        spec = json.loads(cleaned)
        if isinstance(spec, dict) and isinstance(spec.get("nodes"), list) and spec["nodes"]:
            return spec
    except json.JSONDecodeError:
        pass
    return {
        "title": topic,
        "nodes": [{"id": "n1", "label": raw[:180] or topic}],
        "edges": [],
    }
