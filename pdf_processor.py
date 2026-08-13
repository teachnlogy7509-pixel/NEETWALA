
from pathlib import Path
import fitz

def extract_text(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = []
    for page in doc:
        text.append(page.get_text())
    return "\n".join(text)

def detect_chapter(text: str) -> str:
    text = text.lower()
    if "cell" in text or "कोशिका" in text:
        return "कोशिका"
    if "genetics" in text or "आनुवंशिकी" in text:
        return "आनुवंशिकी"
    return "जीवविज्ञान"
