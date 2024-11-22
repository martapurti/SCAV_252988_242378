# Usa una imagen base de Python 3.9
FROM python:3.9

# Dona permís per utilitzar docker
USER root

# Estableix el WorkDirectory a /app
WORKDIR /app

# Copia l'arxiu de requirements al contenidor 
COPY requirements.txt /app/requirements.txt
# Instal·la les dependències
RUN pip install --no-cache-dir -r requirements.txt

# Carpeta amb les imatges
COPY content /app/content 
# Funcions seminari passat (arxiu py)
COPY main.py /app/main.py
# Unit tests
COPY unit_tests.py /app/unit_tests.py

# Instal·lar dependències de Docker
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    lsb-release \
    && curl -fsSL https://get.docker.com | sh

# Copia a l'app
COPY . /app/


# Comando para ejecutar FastAPI usando Uvicorn
# Aquí: Descomentar la segona línea per executar els unit tests
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["python", "-m", "unittest", "unit_tests.py"]