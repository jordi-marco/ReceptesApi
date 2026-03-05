# Versió lleugera de Python
FROM python:3.11-slim

# Evita que Python generi fitxers .pyc i permet veure logs en temps real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instal·lem dependències del sistema per a PostgreSQL (psycopg2)
# RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Instal·lem les dependències de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiem el codi de l'aplicació
COPY . .

# Exposem el port de FastAPI
EXPOSE 8000

# Comanda per executar l'aplicació amb Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]