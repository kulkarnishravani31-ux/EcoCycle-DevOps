# EcoCycle ♻️ — E-waste Pickup & Tracking

A student-ready full-stack DevOps project built with **Python Flask, MySQL, HTML, CSS and JavaScript-ready templates**, Docker, GitHub Actions and automated tests.

## Features
- User registration and secure password hashing
- Login/logout and session-based access
- Book e-waste pickup requests
- User dashboard to track request status
- Admin dashboard to approve, reject or mark collections complete
- Health-check endpoint at `/health`
- MySQL database in Docker Compose; SQLite fallback for quick local development

## Run locally (SQLite)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000. The database is created automatically.

## Run with Docker + MySQL
```bash
docker compose up --build
```
Open http://localhost:5000. In another terminal, create the admin account:
```bash
docker compose exec web flask --app app create-admin
```
Default local admin: `admin@ecocycle.local` / `Admin123!`. Change this immediately for any shared deployment.

Stop containers:
```bash
docker compose down
```
Remove database volume (destructive):
```bash
docker compose down -v
```

## Tests
```bash
pytest -q
```
GitHub Actions runs tests and builds the Docker image on pushes and pull requests to `main`/`master`.

## GitHub workflow demonstration
```bash
git init
git add .
git commit -m "Initial EcoCycle Flask application"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ecocycle-devops.git
git push -u origin main
```
Make a feature branch, commit a change, push it and open a pull request to demonstrate collaboration and CI.

## Deploy (Render)
1. Push this repository to GitHub.
2. In Render, create a **Web Service** from the repository.
3. Choose Docker as the runtime.
4. Set environment variables: `SECRET_KEY` (long random value), `DATABASE_URL` (your managed MySQL connection string), `ADMIN_EMAIL`, `ADMIN_PASSWORD`.
5. Deploy and test `/health`.

A persistent/managed MySQL service is required for durable production data. Do not rely on a local container filesystem for production database storage. Free-tier availability and database offerings change; check current provider limits. This repository includes a Dockerfile suitable for a container web service.

## Environment variables
See `.env.example`. Never commit real secrets or production passwords.

## Suggested team split (5 students)
1. Frontend: pages, styling, responsive UI.
2. Backend: Flask routes, validation and authentication.
3. Database: schema, MySQL configuration and data testing.
4. DevOps: GitHub, Actions, Docker and deployment.
5. QA & documentation: test cases, README, screenshots and project report.

## Important production improvements
This is an educational starter, not a production-certified service. Before real-world use add CSRF protection, rate limiting, email verification/password reset, stronger role provisioning, audit logs, input/output security review, HTTPS-only secure cookies, database migrations, backup/restore procedures and privacy/data-retention controls. Set a strong `SECRET_KEY` and unique admin password.

## Project structure
```
ecocycle_devops/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci.yml
├── templates/
├── static/
├── tests/
└── docs/
```


## Premium frontend update
The refreshed responsive interface includes a sustainability-startup landing page, responsive navigation, polished login/register screens, category-card pickup booking, user dashboard summary cards, request history, admin metrics, request search and status filtering. The UI uses the existing Flask routes and form field names; no API contract or database schema changes are required. Google Fonts are loaded from Google Fonts when internet access is available; the layout remains usable without them.
