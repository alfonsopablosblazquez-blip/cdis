# Usamos imagen base ligera de Python 3.10
FROM python:3.10-slim

# Evita buffering en Python
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Variables de entorno para la base de datos (Render las puede sobrescribir)
ENV DB_HOST=dpg-d4u0hcm3jp1c73f6ued0-a
ENV DB_PORT=5432

# Copiar y instalar dependencias
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copiar todo el código de la app
COPY . .

# Crear carpeta de uploads y darle permisos
RUN mkdir -p /app/uploads && chown -R 1000:1000 /app/uploads || true

# Permisos para wait-for-it
RUN chmod +x /app/wait-for-it.sh

# Exponer el puerto de la app
EXPOSE 5000

# Esperar a que la base de datos esté disponible antes de iniciar Gunicorn
CMD ["/app/wait-for-it.sh", "$DB_HOST:$DB_PORT", "--", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
