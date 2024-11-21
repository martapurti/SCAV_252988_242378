REPORT PRACTICE 1


DOCKERFILE

Per fer aquesta pràctica vam haver de crear un docker file el qual vam anomenar Dockerfile. En aquest, vam establir un directori de treball /app i vam instal·lar ffmpeg. A més a més, dins d'aquest directori, vam copiar tots els arxius de dependència com requirements.txt, la carpeta content (on es troben totes les imatges que hem utilitzat), el nostre main.py on estan declarades totes les funcions que vam fer al seminari 1, i per últim els unit_tests.py. 

Seguidament, encara dins del Dockerfile, vam instal·lar totes les dependències declarades al arxiu requirements i vam afegir un command per executar FastAPI utilitzant Uvicorn: Aquest command inicia un servidor web que serveix l'aplicació definida a main.py amb la instància app. Escolta en totes les interfícies del contenidor al port 8000. Fa que l'aplicació sigui accessible des de el host de Docker 
(mitjançant docker run -p 8000:8000).

Per executar els unit tests, anar a Dockerfile, i descomentar la segona línia:
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["python", "-m", "unittest", "unit_tests.py"]


MAIN.PY

Ara per testejar la nostra API, hem creat diversos endpoints, els quals ens permetran comunicar-nos amb la API a través de sol·licituds, en el nostre cas, POST i GET.

DOCKER-COMPOSE

Finalment, en l'últim pas, se'ns demanava crear un docker-compose. L'objectiu aquí, era connectar el nostre docker file amb un ffmpeg docker. Per fer-ho vam haver de crear un docker nou anomenat Docker_ffmpeg i vam instal·lar el ffmpeg. 

En aquest, amb aquest docker-compose, el nostre Dockerfile depèn del Docker_ffmpeg, on tots dos tenen accés a la carpeta Content.

Per la utilització de la API, fer docker-compose up --build, i anar a localhost:8000/docs. Aquí es trobaran algunes funcions del main.py per interactuar amb elles. 



