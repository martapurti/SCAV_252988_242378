# Usa una imagen base de Python 3.9
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala ffmpeg
RUN apt-get update && apt-get install -y ffmpeg


# Copia el archivo de dependencias (requirements.txt) y el código al contenedor
COPY requirements.txt /app/requirements.txt
# Carpeta amb les imatges
COPY content /app/content 
# Seminari passat
COPY main.py /app/main.py

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar FastAPI usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
