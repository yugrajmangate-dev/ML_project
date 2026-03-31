# Architecture & Production Checklist

Goal: production-grade, scalable recommendation service with reproducible model packaging and safe DB management.

Core components
- Web API: Flask app served by Gunicorn (Docker). Move to an app factory pattern for testability.
- Model: `recommendation_model.pkl` stored alongside release artifacts or in an object store (S3) with versioning.
- Database: MySQL for users/products/interaction. In production use managed RDS or Cloud SQL.
- Cache: Redis for caching recommendation responses and rate-limiting.
- Background Jobs: Celery + Redis/RabbitMQ for heavy preprocessing, periodic re-training, and async tasks.

Operational concerns
- Containerization: Dockerfile + docker-compose for local dev; CI builds multi-arch Docker images.
- Secrets: inject via environment variables or secrets manager (do NOT commit `.env`).
- Migrations: use Alembic to track DB schema changes (avoid `db.create_all()` in production).
- Monitoring: structured logs (JSON), Prometheus metrics and Grafana dashboards, alerting.
- Error Reporting: Sentry (or similar) for runtime exceptions.
- Security: HTTPS termination (load balancer), input validation, rate limits, least-privilege DB credentials.

Data & Model lifecycle
- Model versioning: store model metadata (version, training data snapshot, eval metrics).
- Periodic retraining: schedule jobs to retrain offline and publish new model artifact.
- Evaluation: maintain holdout metrics and canary releases before full rollout.

CI/CD checklist
- Linting & unit tests run on PRs (pytest, flake8/ruff).
- Build Docker image and run integration tests in CI.
- Push artifacts to container registry and tag by semantic version.
- Deploy using CI to staging, run smoke tests, then promote to production.

Next recommended implementation steps
1. Add Dockerfile & docker-compose (done).
2. Refactor to app factory + create JSON API endpoints for recommendations.
3. Add Alembic migrations and remove unconditional `db.create_all()` from runtime.
4. Add Redis caching and a `/health` endpoint.
5. Add CI workflow and tests.
