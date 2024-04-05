# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos y lo instala
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia el código de tu aplicación
COPY . .

# Expone el puerto 8000 en el contenedor
EXPOSE 8000

# Comando para ejecutar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]