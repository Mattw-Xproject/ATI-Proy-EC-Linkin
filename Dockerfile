FROM python:3.12.4-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

COPY . .

# Asegura que el directorio /data exista para SQLite
RUN mkdir -p /data && chmod 777 /data

# Aplica las migraciones y arranca Gunicorn en el puerto 8000
CMD ["sh", "-c", "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
