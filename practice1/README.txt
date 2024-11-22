REPORT PRACTICE 1

Per aquesta pràctica utilitzem diversos fitxers:

1) MAIN.PY

En aquest arxiu hem creat 3 endpoints, els quals ens permetran comunicar-nos amb la API a través de sol·licituds HTTP, concretament POST i GET. Aquests ens permetran testejar i interactuar les funcions del seminari 1. 

2) UNIT_TESTS.PY

Inclou els unit tests del seminari 1.

3) REQUIREMENTS.TXT

L'arxiu requirements.txt inclou totes les dependències necessàries per executar el codi.

4) DOCKERFILE (API)

Aquest fitxer configura un contenidor per l'API. Creació d'un Docker File anomenat Dockerfile (per la API). En aquest, vam definir un directori de treball /app. 

Dins d'aquest directori, vam copiar tots els arxius: 
- requirements.txt
- la carpeta content (on es troben totes les imatges que hem utilitzat)
- main.py (on estan declarades totes les funcions que vam fer al seminari 1)
- unit_tests.py. 

L'arxiu requirements.txt inclou totes les dependències necessàries per executar el codi. Per aquest motiu, vam instal·lar-les. 

A més, per facilitar l'ús de Docker, es configuren les dependències corresponents i es defineix l'usuari root per garantir els permisos necessaris.

Al final del Dockerfile, hi ha dos comandos:
1- Comando per executar el fastapi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
Per executar el fastapi, vam afegir un comando utilitzant 'uvicorn'. D'aquesta manera podem iniciar un servidor web que serveix l'aplicació definida a main.py amb la instància app. Escolta en totes les interfícies del contenidor al port 8000 (que hem definit nosaltres). Fa que l'aplicació sigui accessible des de el host de Docker 
(mitjançant docker run -p 8000:8000).

2- Comando per executar els unit tests
CMD ["python", "-m", "unittest", "unit_tests.py"]
Per provar els tests, s'ha de comentar el primer comando i descomentar aquest.


5) DOCKER-COMPOSE.YAML

Finalment, en l'últim pas, se'ns demanava crear un docker-compose. Per fer-ho vam haver de crear un docker nou anomenat 6) Docker_ffmpeg i vam instal·lar el ffmpeg. Aquest, executa un comando infinitament per assegurar que el contenidor estigui operatiu mentre es fa servir l'API (CMD ["bash", "-c", "tail -f /dev/null"]).

En el docker-compose, definim els dos serveis que s'han de coordinar: ffmpeg i fastapi. Tots dos tenen accés a la carpeta content. En aquest, el fastapi depèn del ffmpeg: volem que s'iniciï primer el ffmpeg, perquè el contenidor API el necessita. 

Per la utilització de la API, obrim una terminal amb docker-compose up --build, i obrim un buscador amb  localhost:8000/docs. Aquí es trobaran els endpoints, funcions del main.py per interactuar amb elles. 







