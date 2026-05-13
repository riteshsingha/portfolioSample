# Portfolio Backend — FastAPI Contact API

A small, focused FastAPI service that powers the **Send Message** form on the portfolio. Validates the payload, blocks bots via a honeypot + rate limit, and delivers the message to your Gmail inbox via SMTP.

- **Stack:** FastAPI · Pydantic v2 · slowapi · stdlib `smtplib`
- **Endpoint:** `POST /api/contact`
- **Health:** `GET /api/health`
- **Docs:** `GET /docs` (Swagger), `GET /redoc`

---

## Folder structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + CORS + slowapi wiring
│   ├── config.py            # Settings loaded from .env
│   ├── schemas.py           # Pydantic ContactIn / ContactOut
│   ├── email_service.py     # SMTP delivery (Gmail)
│   └── routes/
│       ├── __init__.py
│       └── contact.py       # POST /api/contact
├── .env.example
├── .gitignore
├── requirements.txt
├── run.ps1                  # Windows helper
└── README.md
```

---

## 1. Set up a Gmail App Password (one-time, 2 minutes)

Gmail no longer accepts your normal password over SMTP. You need a **16-character App Password**.

1. Open <https://myaccount.google.com/security>.
2. Under **How you sign in to Google**, enable **2-Step Verification** (if it isn't already).
3. Go to <https://myaccount.google.com/apppasswords>.
4. App: pick **Mail**. Device: **Other (Custom name)** → type `Portfolio Backend`.
5. Click **Generate**. Copy the 16-character code (spaces don't matter — paste them or strip them, both work).

> Keep this password secret. It only authorizes SMTP access, not full account login.

---

## 2. Configure environment

```powershell
cd backend
copy .env.example .env
notepad .env
```

Fill in:

```dotenv
SMTP_USER=hriteshsingha@gmail.com
SMTP_PASSWORD=abcdwxyz12345678        # the App Password from step 1
MAIL_TO=hriteshsingha@gmail.com       # where messages land (any inbox)
CORS_ORIGINS=http://localhost:8080,http://127.0.0.1:5500
```

`.env` is git-ignored — it will never be committed.

---

## 3. Install & run

### Windows (PowerShell, one-liner)

```powershell
.\run.ps1
```

The helper creates `venv/`, installs deps, checks `.env`, and starts uvicorn on **http://127.0.0.1:8000**.

### Manual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## 4. Verify

```powershell
# Health
curl http://127.0.0.1:8000/api/health
# → {"status":"ok","smtp_configured":true}

# Send a test message
curl -X POST http://127.0.0.1:8000/api/contact `
     -H "Content-Type: application/json" `
     -d '{
           "name":    "Curl Tester",
           "email":   "tester@example.com",
           "subject": "Hi from curl",
           "message": "This is a backend smoke test."
         }'
```

Check your Gmail inbox — the message arrives within seconds, with **Reply-To** set to the sender's address so hitting Reply in Gmail just works.

You can also explore the auto-generated Swagger UI at <http://127.0.0.1:8000/docs>.

---

## 5. Wire the frontend

`script.js` already POSTs JSON to the backend. Open it and confirm:

```js
const ENDPOINT = 'http://127.0.0.1:8000/api/contact';
```

When you deploy, change it to your public backend URL (and add that domain to `CORS_ORIGINS`).

---

## Anti-spam features

| Layer            | What it does                                                                |
|------------------|------------------------------------------------------------------------------|
| Pydantic         | Strict types, length bounds, `EmailStr` validation                          |
| Honeypot         | Hidden `website` field — bots fill it, humans don't. Silently dropped.       |
| Rate limit       | `5/minute` per IP via slowapi (configurable in `.env`)                      |
| CORS allowlist   | Only origins in `CORS_ORIGINS` can POST                                      |
| Reply-To header  | Reply in Gmail goes to the sender, not back to your own SMTP account         |

---

## Deploy

The app is a standard ASGI service — runs anywhere uvicorn does:

- **Render / Railway / Fly.io** — `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Docker** — base image `python:3.12-slim`, copy + install + run.
- **Bare VPS** — uvicorn behind nginx + systemd.

Set the env vars (`SMTP_USER`, `SMTP_PASSWORD`, `MAIL_TO`, `CORS_ORIGINS`) in your provider's dashboard — **don't ship `.env`**.

---

## Troubleshooting

| Symptom                                            | Fix                                                                                   |
|----------------------------------------------------|---------------------------------------------------------------------------------------|
| `502 Bad Gateway` from `/api/contact`              | `.env` missing or wrong. Check `/api/health` → `smtp_configured`.                     |
| `SMTPAuthenticationError`                          | Wrong App Password, or 2-Step Verification not enabled on Google.                     |
| Frontend POST blocked with `CORS error`            | Add the frontend origin to `CORS_ORIGINS` and restart the server.                     |
| `429 Too Many Requests`                            | You hit the rate limit. Adjust `RATE_LIMIT` in `.env` or wait a minute.               |
| Mail in "All Mail" but not "Inbox"                 | Gmail filtered it as Promotions. Mark as "Not promotions" once.                       |
