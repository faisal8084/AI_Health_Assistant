# AI Health Assistant

FastAPI backend jo diabetes, heart disease, aur mental-health-treatment risk
predict karta hai — ek direct REST API se, ya ek Gemini-powered conversational
chatbot se.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env      # phir .env mein apna GEMINI_API_KEY, DATABASE_URL, SECRET_KEY daalein
```

Apni trained model files `models/` folder mein daalein — dekhein
`models/README.md` mein exact filenames.

### PostgreSQL (for login/signup)

Make sure PostgreSQL is running and the database in `DATABASE_URL` exists, e.g.:

```bash
createdb ai_health_assistant
```

Generate a real secret key for `.env`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

The `users` table is created automatically on startup — no manual migration needed.

## Run

```bash
uvicorn main:app --reload
```

Docs: `http://127.0.0.1:8000/docs`

Serve the frontend (any static file server works) and open it in the browser:

```bash
cd frontend
python -m http.server 5500
# then open http://127.0.0.1:5500/login.html
```

First-time users should hit **Create Account** on the login page. Every
page except `login.html` / `register.html` now requires a valid session —
you'll be redirected to `login.html` automatically if you're signed out.
Use the gear icon to point the frontend at your backend URL if it's not
running on `http://127.0.0.1:8000`.

## Authentication

```
POST /auth/register   { name, email, password, confirm_password } -> user
POST /auth/login       { email, password } -> { access_token, token_type }
GET  /auth/me          (Authorization: Bearer <token>) -> user
POST /auth/logout      (Authorization: Bearer <token>) -> { success, message }
```

* Passwords are hashed with **bcrypt** (via `passlib`) — never stored in plain text.
* Sessions are stateless **JWTs**, signed with `SECRET_KEY` and expiring after
  `ACCESS_TOKEN_EXPIRE_MINUTES` (default 60).
* `/predict/*`, `/predict/health`, `/chat`, and `/chat/reset` all now require
  a valid `Authorization: Bearer <token>` header — unauthenticated requests
  get a `401`.
* The frontend stores the token in `localStorage` and attaches it to every
  API call automatically (see `frontend/scripts/api.js`); a `401` response
  clears it and bounces the user back to `login.html`.

## Project structure

```
main.py                        # FastAPI app + routes
backend/
  database.py                  # SQLAlchemy engine/session (NEW)
  dependencies.py               # get_current_user JWT dependency (NEW)
  models/user.py                # users table (NEW)
  routers/auth.py               # /auth/* endpoints (NEW)
  schemas/                     # Pydantic request/response models (+ auth.py, NEW)
  services/                    # model-loading + prediction logic (+ auth_service.py, NEW)
src/
  prediction_engine.py         # single entrypoint used by both API & chatbot
  chatbot/                     # conversational flow (Gemini-backed)
models/                        # apni .pkl/.ubj/.txt model files yahan
frontend/
  login.html, register.html    # auth pages (NEW)
  index.html                   # protected app shell (requires login)
  scripts/theme.js              # dark/light mode toggle (NEW)
  scripts/auth-guard.js         # redirects to login if signed out (NEW)
  scripts/auth-page.js          # login/register form logic (NEW)
  styles/auth.css               # auth page styling (NEW)
```

## Bugs jo fix kiye gaye (changelog)

Project ko run karne layak banane ke liye yeh saare issues fix kiye gaye hain:

1. **Missing `src/chatbot/intent.py`** — `chatbot_engine.py` isko import
   karta tha (`from src.chatbot.intent import detect_intent`) lekin file
   kahin exist hi nahi karti thi → app start hote hi `ModuleNotFoundError`
   se crash ho jaata. Ab yeh file ek simple keyword-based fallback intent
   detector ke saath bana di gayi hai.

2. **Missing Python package structure** — koi `__init__.py` files nahi thi
   aur files flat structure mein thi, jabki code
   `backend.schemas.diabetes`, `src.chatbot.chatbot_engine` jaise dotted
   imports use karta tha. Ab proper `backend/`, `src/`, `src/chatbot/`
   packages bana di gayi hain.

3. **Diabetes chatbot flow ka guaranteed `KeyError`** — `age_group` aur
   `bmi_category` `AUTO_FIELDS` mein listed the (matlab chatbot kabhi
   yeh questions nahi puchta), lekin inhe compute karne wala code kahin
   nahi tha. Isliye chatbot se koi bhi diabetes prediction
   `predict_diabetes()` ke andar `KeyError` de kar fail ho jaati.
   Fix: `src/chatbot/fields.py` mein `get_age_group()` /
   `get_bmi_category()` add kiye, jo `src/prediction_engine.py` age/bmi
   se automatically compute karta hai.

4. **Heart aur Treatment chatbot flow mein field-name mismatch (bada bug)**
   — `questions.py` field names use karta hai jaise `chest_pain_type`,
   `age` (treatment ke liye), lekin baaki poora system (`fields.py`,
   `validator.py`, model services) canonical names use karta hai jaise
   `chest pain type` (space wala), `Age` (capital wala). Purana code
   answer ko RAW naam se save karta tha, canonical naam se nahi — isse:
   - validation (range checks / allowed-values checks) silently skip ho
     jaati thi kyunki raw naam kisi bhi table mein match hi nahi karta
     tha,
   - final prediction call mein `self.state.data` mein galat keys hoti
     thi, aur `predict_heart_dieses()` / `predict_treatment()` `KeyError`
     de kar fail ho jaate the.

   Fix: `chatbot_engine.py` ab field ko canonical naam mein convert
   karke hi validate/store karta hai, aur `questions.py` ka
   `next_question()` bhi ab canonical naam se hi check karta hai ki
   sawaal already answered hai ya nahi (warna infinite loop ban jaata).

5. **Treatment ke "yes/no" fields galat type mein convert ho rahe the** —
   `validator.py` `self_employed`, `remote_work`, `tech_company`,
   `mental_health_consequence`, etc. ko `1`/`0` integer mein convert kar
   raha tha, jabki `backend/schemas/treatment.py` aur trained model
   inhe exact strings ("Yes"/"No"/"Maybe"/"Don't know" etc.) expect karte
   hain. Isse har treatment prediction fail ho jaati (ya galat result
   deti). Saath hi `family_history` field bilkul handle hi nahi ho rahi
   thi. Fix: naya `TREATMENT_FIELD_OPTIONS` table add kiya jo har
   treatment field ko uske sahi allowed string values mein normalize +
   validate karta hai.

6. **`smoking_history` casing normalize nahi hoti thi** — validation
   case-insensitive thi lekin stored value original casing mein hi rehti
   thi (e.g. "Never" instead of "never"), jo trained preprocessor ke liye
   unseen category ban sakti thi. Ab canonical casing mein normalize hota
   hai.

7. **`chest_pain_type` range mismatch** — schema
   (`heart_dieses.py`) `Literal[1, 2, 3, 4]` expect karta tha lekin
   chatbot validator ki range `(0, 3)` thi. Dono ko `1–4` par align kar
   diya.

8. **Confusing typo field `st_pepression`** — heart schema mein rename
   karke `oldpeak` kar diya (poore codebase mein baaki jagah yahi naam
   use ho raha tha — Gemini extraction, `questions.py`, `fields.py`).
   `heart_dieses_service.py` se ab is field ke liye extra/unnecessary
   rename step bhi hata diya gaya.

9. **Response typos** — `/predict/heartDieses` aur `/predict/treatment`
   endpoints "succes"/"diease" return kar rahe the — fix karke
   "success"/"disease" kiya (client-side JSON parsing consistent ho).

10. **`/predict/health` endpoint** unsupported condition par generic
    500 "Internal server error" deta tha (`ValueError` uncaught tha) —
    ab proper `400` deta hai jaise `/chat` endpoint karta hai.

11. **Duplicate `from fastapi import FastAPI` import** — cleanup kiya.

## Note

Actual trained model files (`.pkl` / `.ubj` / `.txt`) is upload mein nahi
thi, isliye woh is zip mein nahi hain — `models/README.md` dekhein.
