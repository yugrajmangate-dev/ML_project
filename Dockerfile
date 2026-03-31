FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install build deps needed for some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app sources
COPY . .

EXPOSE 5000

# Use Gunicorn to run the Flask app (app:app)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "3"]
