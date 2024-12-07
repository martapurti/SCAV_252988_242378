
PRACTICE 2

Per aquesta pràctica crearem un nou fitxer: index.html, on hi haurà el front-end per la nostra Monster API. 
Dins ens trobarem com hem definit la pàgina, i com interactua aquesta amb el nostre back-end (main.py) on es troben definides les nostres funcions.
Per executar-ho obrirem una terminal en el directori del projecte (practice2, en el nostre cas), i després de fer docker-compose up --build, posarem: 
python -m http.server per poder accedir a la nostre GUI que hem creat en l'arxiu .html

Obrirem el buscador amb localhost:8000 per la seva visualització.

Per utilitzar la GUI cal utilitzar el contigut guardat a la carpeta content!

Per testejar els endpoints, obrirem el buscador amb localhost:5000/docs i utilitzarem el Swagger que ens proporciona FastAPI.

Per VP8 i VP9, utilitzarem .WebM container, basat en un perfil de Matroska,.mp4 container no suporta aquests còdecs.
AV1 té el temps de codificació més alt.

Els fitxers resultants es guarden a la carpeta content. 

Mencionar també que tant els unit_tests com la GUI triguen bastant en executar-se.





