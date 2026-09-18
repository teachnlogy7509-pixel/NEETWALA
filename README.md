# NEETWALA Knowledge Bot

यह Telegram bot Hindi NEET Biology के लिए AI knowledge, short-notes और educational diagram assistant है।

## मुख्य सुविधाएँ

- `/knowar` से Hindi में concept explanation
- `/notesar` से exam-ready short notes
- `/diagramaar` से topic का generated educational SVG diagram
- OpenRouter → Groq → Gemini AI fallback chain
- PDF को Telegram Document के रूप में भेजने पर text extraction और short notes
- Latest PDF का translation: `/translatepdfar English`
- किसी replied message का translation: `/translatear English`
- हर user का chat ID, username, name, language और last-seen SQLite में save
- Admin broadcast: `/broadcast संदेश` या किसी message को reply करके `/broadcast`
- Admin user list: `/usersar`
- Admin CSV export: `/exportusersar`
- Leaderboard हटाकर knowledge और user-management पर focus

## AI keys

Railway Variables में इनमें से कम से कम एक provider की key लगाएँ:

```text
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openrouter/auto
GROQ_API_KEY=...
GROQ_MODEL=llama-3.3-70b-versatile
GEMINI_API_KEY_1=...
```

Bot पहले OpenRouter, फिर Groq, फिर Gemini try करता है। Keys code या GitHub में commit न करें।

## Short notes और diagram

```text
/notesar कोशिका
/diagramaar परागण और निषेचन
```

किसी Telegram text message को reply करके `/notesar` लिखने पर उसी text के short notes बनेंगे। `/diagramaar` एक educational SVG file बनाता है जिसे browser में खोला जा सकता है।

## Setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Required values:

```text
TELEGRAM_BOT_TOKEN=...
ADMIN_CHAT_IDS=123456789
```

Admin chat ID जानने के लिए bot में `/id` भेजें।

## PDF

PDF को Telegram में **Document** के रूप में भेजें। Bot extracted text save करेगा, chapter पहचानेगा और Hindi short notes बनाएगा। Scanned/image-only PDFs में OCR अलग से जोड़ना होगा।

## Privacy

User records और extracted PDF text local SQLite database में save होते हैं। Production deployment में database disk को persistent volume दें और `.env` को GitHub पर commit न करें।
