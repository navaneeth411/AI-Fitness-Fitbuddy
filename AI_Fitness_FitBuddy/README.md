
# FitBuddy – AI Fitness Plan Generator

## Project
A web-based AI fitness application that generates personalized 7-day workout plans and nutrition/recovery tips. Users can submit feedback and receive an updated plan.

## Technology
- Python
- FastAPI
- Google Gemini API
- HTML/CSS/Jinja2
- SQLite
- SQLAlchemy
- Uvicorn

## Folder Structure
```text
AI_Fitness_FitBuddy/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── gemini_service.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── result.html
│   │   ├── all_users.html
│   │   └── message.html
│   └── static/css/style.css
├── requirements.txt
├── .env.example
└── README.md
```

## Run on Windows
Open Terminal/PowerShell in this folder:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file from `.env.example` and put your Gemini API key in it.

Then run:
```powershell
uvicorn app.main:app --reload
```

Open:
`http://127.0.0.1:8000`

Admin view:
`http://127.0.0.1:8000/view-all-users`

API docs:
`http://127.0.0.1:8000/docs`

## Important
Do not upload your real Gemini API key to GitHub. Keep it in `.env`.

The application includes a fallback demo plan if an API key is not configured, so the interface can still be demonstrated locally. For a genuine Gemini-powered result, configure `GOOGLE_API_KEY`.
