FROM python:3.11-slim-bullseye

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y pkg-config\
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements/base.txt

EXPOSE 8000

# Exponer el puerto y definir el comando de inicio
CMD ["sh", "-c", "python ToDo/manage.py runserver 0.0.0.0:$PORT"]