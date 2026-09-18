# NEETWALA Knowledge Bot

यह Telegram bot अब केवल quiz bot नहीं है; यह Hindi NEET Biology knowledge assistant है।

## नई सुविधाएँ

- `/knowar` से Hindi में concept explanation
- Gemini से topic और chapter-based NEET MCQ
- PDF को Telegram Document के रूप में भेजने पर text extraction
- PDF chapter detection और Hindi study notes
- Latest PDF का translation: `/translatepdfar English`
- किसी replied message का translation: `/translatear English`
- हर user का `chat_id`, username, name, language और last-seen SQLite में save
- Admin broadcast: `/broadcast संदेश` या किसी message को reply करके `/broadcast`
- Admin user list: `/usersar`
- Admin CSV export: `/exportusersar`
- Leaderboard हटाकर knowledge और user-management पर focus

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

## Commands

```text
/knowar कोशिका को आसान भाषा में समझाओ
/quizar कोशिका 30
/chapterar आनुवंशिकी 30
```

PDF को Telegram में **Document** के रूप में भेजें। Bot extracted text save करेगा, chapter पहचानेगा और Hindi notes बनाएगा। फिर latest PDF के लिए:

```text
/translatepdfar English
```

Scanned/image-only PDFs में selectable text नहीं होने पर OCR अलग से जोड़ना होगा।

## Privacy

User records और extracted PDF text local SQLite database में save होते हैं। Production deployment में database disk को persistent volume दें और `.env` को GitHub पर commit न करें।
