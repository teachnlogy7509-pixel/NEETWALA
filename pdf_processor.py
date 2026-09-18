import fitz


def extract_text(pdf_path: str) -> str:
    pages = []
    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            page_text = page.get_text("text").strip()
            if page_text:
                pages.append(f"[Page {page_number}]\n{page_text}")
    return "\n\n".join(pages).strip()


def detect_chapter(text: str) -> str:
    lowered = text.lower()
    patterns = {
        "कोशिका": ["cell", "कोशिका", "mitochondria", "माइटोकॉन्ड्रिया"],
        "आनुवंशिकी": ["genetics", "आनुवंशिकी", "dna", "डीएनए", "heredity"],
        "पारिस्थितिकी": ["ecology", "पारिस्थितिकी", "ecosystem", "ecosystem"],
        "मानव शरीर": ["human physiology", "मानव शरीर", "digestion", "श्वसन", "circulation"],
        "पादप शरीर": ["plant physiology", "पादप", "photosynthesis", "प्रकाश संश्लेषण"],
    }
    for chapter, keywords in patterns.items():
        if any(keyword in lowered for keyword in keywords):
            return chapter
    return "जीवविज्ञान"
