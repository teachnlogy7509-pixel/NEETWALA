# NEETWALA Knowledge Bot

यह Telegram bot Hindi NEET Biology के लिए Gemini-style knowledge और short-notes assistant है।

## मुख्य सुविधाएँ

- `/knowar` से Hindi में concept explanation
- `/notesar` से किसी topic के exam-ready short notes
- किसी text message को reply करके `/notesar` लिखने पर उसी text के short notes
- Gemini से topic और chapter-based NEET MCQ
- PDF को Telegram Document के रूप में भेजने पर text extraction
- PDF chapter detection और Gemini-style Hindi short notes
- Latest PDF का translation: `/translatepdfar English`
- किसी replied message का translation: `/translatear English`
- हर user का `chat_id`, username, name, language और last-seen SQLite में save
- Admin broadcast: `/broadcast संदेश` या किसी message को reply करके `/broadcast`
- Admin user list: `/usersar`
- Admin CSV export: `/exportusersar`
- Leaderboard हटाकर knowledge और user-management पर focus

## Short notes कैसे बनेंगे?

Topic के लिए:

```text
/notesar कोशिका
```

किसी Telegram text को summarize करने के लिए उस message पर reply करें:

```text
/notesar
```

Bot title, concept, definitions, key points, जरूरी comparison, process/formula, NEET exam points और mnemonic/trick के साथ लगभग 500-700 words के concise notes देगा।

## Setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

`.env` में ये values भरें:

```text
TELEGRAM_BOT_TOKEN=...
GEMINI_API_KEY_1=...
ADMIN_CHAT_IDS=123456789
```

Admin chat ID जानने के लिए bot में `/id` भेजें। `ADMIN_CHAT_IDS` में comma-separated IDs लिख सकते हैं।

## PDF

PDF को Telegram में **Document** के रूप में भेजें। Bot extracted text save करेगा, chapter पहचानेगा और short notes बनाएगा। फिर latest PDF के लिए:

```text
/translatepdfar English
```

Scanned/image-only PDFs में selectable text नहीं होने पर OCR अलग से जोड़ना होगा।

## Privacy

User records और extracted PDF text local SQLite database में save होते हैं। Production deployment में database disk को persistent volume दें और `.env` को GitHub पर commit न करें।
