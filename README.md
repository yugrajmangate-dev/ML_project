# E-Commerce Product Recommendation Engine
## E-Commerce Recommendation Service — Production-ready Starter

This repository contains a hybrid recommendation engine and a simple web UI built with Flask. It is designed as a practical, production-ready codebase that can be extended for real-world use.

Core idea
- Hybrid recommender:
  - Collaborative filtering (user-based) — recommends items based on similar users' behavior.
  - Content-based filtering — item similarity computed with TF-IDF over product descriptions and cosine similarity.

What this repo provides
- Web application with user auth, product browsing, and a dashboard that surfaces personalized recommendations.
- A versioned model artifact (`recommendation_model.pkl`) used by the `Recommender` class.
- Scripts and utilities to populate a MySQL database (`setup_db.py`).
- Dockerfile and `docker-compose.yml` for local parity and easier deployment.
- JSON API endpoints for programmatic recommendations (`/api/recommend/collab`, `/api/recommend/content`) and a `/api/health` endpoint.

Quickstart (local, development)
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Optional: populate a local MySQL instance (this will DROP and recreate the database named in `DB_NAME`):
```bash
# Edit .env or set DB_* environment variables first
python setup_db.py
```
3. Start the app (development):
```bash
python app.py
# OR using Docker
docker-compose up --build
```
4. Open `http://localhost:5000` and register a user. To trigger collaborative recommendations immediately, optionally set the `Customer ID` field on the user profile to a known ID (for example `17850`) from the dataset.

API examples
- Collaborative recommendations:
  - GET `/api/recommend/collab?customer_id=17850&n=8`
- Content recommendations:
  - GET `/api/recommend/content?q=85048&n=5`

Recommended next steps for production hardening
- Replace `db.create_all()` with Alembic migrations and use a managed RDS instance.
- Add Redis caching for recommendation results and rate-limiting on the API.
- Run the app with Gunicorn behind a reverse proxy (Nginx) and enable TLS.
- Add CI to run unit and integration tests and build/publish container images.

If you want, I will next refactor the codebase to add Alembic migrations, implement Redis caching, and create a GitHub Actions CI pipeline. Tell me which to prioritize.
