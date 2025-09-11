FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app & model artifact into the image
COPY app.py model.joblib ./

EXPOSE 8080
CMD exec gunicorn --bind :$PORT --workers 1 --threads 2 --timeout 120 app:app
