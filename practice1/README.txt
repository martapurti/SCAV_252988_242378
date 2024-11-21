REPORT PRACTICE 1

Per fer aquesta pràctica vam haver de crear un docker file el qual vam anomenar Dockerfile. En aquest, vam establir un
directori de treball /app i vam instal·lar ffmpeg. A més a més, dins d'aquest directori, vam copiar tots els archius de
dependència com requirements.txt, la carpeta content (on es troben totes les imatges que hem utilitzat), i per últim el
nostre main.py on estan declarades totes les funcions que vam fer al seminari 1.

Seguidament, encara dins del dockerfile, vam instal·lar totes les dependencies declarades al archiu requirements i finalment,
vam afegir un command per executar FastAPI utilitzant Uvicorn.

Aquest command inicia un servidor web que serveix l'aplicació definida a main.py amb la instància app. Escolta en totes les 
interfícies del contenidor al port 8000. Fa que l'aplicació sigui accessible des de el host de Docker 
(mitjançant docker run -p 8000:8000).

Ara per testejar la nostra API, hem creat diveros endpoints, els quals ens permetran comunicarnos amb la API a través de
solicituds com per exemple, POST.

Finalment, en l'últim pas, se'ns demanava crear un docker-compose. L'objectiu aquí, era connectar el nostre docker file amb 
un ffmpeg docker. Per fer-ho vam haver de crear un docker nou anomenat. Docker_ffmpeg i vam instal·lar el ffmpeg. 

En aquest, amb aquest docker-compose, el nostre Dockerfile depen del Docker_ffmpeg, i hem posat compartida la carpeta 
de content per a que puguin accedir tots dos a les imatges.

Per l'utilització de la API, fer docker-compose up --build, i anar a localhost:8000/docs. Aquí es trobaran algunes funcions del main.py per interactuar amb elles. 

Per executar els unit tests, anar a Dockerfile, i descomentar la segona línia.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["python", "-m", "unittest", "unit_tests.py"]
