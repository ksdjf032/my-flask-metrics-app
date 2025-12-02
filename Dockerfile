# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps (optional but prevents some build issues)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first (better Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY src ./src

# Expose port (Fly.io will respect this)
EXPOSE 8080

# Environment defaults
ENV PORT=8080
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Launch using gunicorn
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8080", \
     "src.app:app", \
     "--workers", "2", \
     "--worker-class", "gthread", \
     "--threads", "4"]
