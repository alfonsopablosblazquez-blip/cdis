FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar y instalar dependencias
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copiar todo el código
COPY . .

# Crear carpeta de uploads y permisos
RUN mkdir -p /app/uploads && chown -R 1000:1000 /app/uploads || true

# Copiar wait-for-it.sh y darle permisos
RUN chmod +x /app/wait-for-it.sh

# Exponer puerto de la app
EXPOSE 5000

# Usar wait-for-it para esperar a la base de datos antes de arrancar Gunicorn
CMD ["/app/wait-for-it.sh", "db:5432", "--", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
