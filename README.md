# Credits Management API (FastAPI + PostgreSQL)

Tracks user credits (add, deduct, reset), exposes query/update endpoints, and runs a daily job to add +5 credits to all users at 00:00 UTC. Includes an admin-only schema update API.

## Features
- Users & credits tables (see `schema.sql`)
- Endpoints:
  - `GET /api/credits/{user_id}`
  - `POST /api/credits/{user_id}/add` (body: `{ "amount": number }`)
  - `POST /api/credits/{user_id}/deduct` (no negatives)
  - `PATCH /api/credits/{user_id}/reset`
  - `PATCH /api/schema/update` (admin-only, apply SQL)
- Background task: +5 credits to all users daily @ midnight UTC
- Postman collection included

## Setup

1) Create DB and apply schema:
```bash
psql -U postgres -c "CREATE DATABASE credits_db;"
psql -U postgres -d credits_db -f schema.sql
Create .env from example:

bash
Copy code
cp .env.example .env
# edit DATABASE_URL and ADMIN_TOKEN as needed
Create virtual env & install deps:

bash
Copy code
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
Run the server:

bash
Copy code
uvicorn src.main:app --reload
Docs: http://127.0.0.1:8000/docs

Health: http://127.0.0.1:8000/api/health

Postman
Import credits_api.postman_collection.json and use the requests.
Set baseUrl to your server and adminToken to your ADMIN_TOKEN value.

Notes
The schema update endpoint requires header: X-Admin-Token: <ADMIN_TOKEN>.

The scheduler runs in-process (APScheduler) and uses UTC.

yaml
Copy code

---

## ✅ What to do next

1) Create DB and apply schema:
```powershell
psql -U postgres -c "CREATE DATABASE credits_db;"
psql -U postgres -d credits_db -f schema.sql
Create .env:

env
Copy code
DATABASE_URL=postgresql+psycopg2://postgres:Kamal%401234@localhost:5432/credits_db
ADMIN_TOKEN=super_secret_admin_token
Install & run:

powershell
Copy code
python -m venv .venv
. .venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload