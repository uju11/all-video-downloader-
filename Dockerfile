FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for yt-dlp
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/

# Create downloads directory
RUN mkdir -p downloads

EXPOSE 5000

CMD ["gunicorn", "--workers=1", "--worker-class=gthread", "--threads=4", "--timeout=120", "--bind=0.0.0.0:5000", "app:app"]
