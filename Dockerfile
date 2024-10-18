# Imagen base
FROM python:3.10-slim

# Configurar variable de entorno
ENV workdir=/app

# Crear directorio de trabajo
RUN mkdir -p $workdir

# Carpeta de trabajo
WORKDIR $workdir

# Copiar todo el proyecto al directorio home de Docker
COPY . $workdir

# Actualizar pip
RUN pip install --upgrade pip

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Puerto donde se ejecuta la aplicación Django
EXPOSE 8000

# Definir el comando para ejecutar la aplicación (ajustar según sea necesario)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]