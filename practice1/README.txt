A veure, apunto per a que no se m'oblidi:

He modificat el Dockerfile i li he tret que es descarregui el ffmpeg.

Ara, per poder utilizar el ffmpeg, he fet "pull" de la següent imatge publica de ffmpeg (fer-ho a la terminal amb el directori del projecte): docker pull jrottenberg/ffmpeg

Aquest docker ja te totes les funcionalitas de ffmpeg ;)

Ara l'objectiu es crear un docker-compose, que al executar-se comuniqui el docker jrottenberg/ffmpeg (el que acabem de descarregar) amb el nostre Dockerfile per poder seguir utilitzant les funcions amb el ffmpeg

He creat el docker-compose (el chat me l'ha fet) on suposadament ja es connecten.

Ara, per executar aquest, he fet: 
docker-compose up --build
(Només amb això executa el docker-compose, que aquest mateix també executa el nostre Dockerfile)

He afegit un endpoint de la tasca 3 per veure si funciona el ffmpeg. Vas a localhost:8000/docs i surt bé :)

L'unic, que el chat m'ha fet crear una classe per aquesta tasca per comprobar que els inputs estàn bé. Llavors si introduïm dades valides, suposadament hauria de funcionar i en cas de dades invalides surt un missatge de: "Error al processar la imatge" o algo així.

S'ha de comprobar la classe pq el chat m'ha dit de posar strings com a input d'imatge, i doncs no entenc com vol fer resize d'una string (ho he provat i no hem deixa).

Conclusió, el docker-compose sembla que xuta sense problemes pero estaria bé fer un endpoint amb una tasca que es necessiti el ffmpeg per quedar com unes reines, així que s'hauria de mirar d'arreglar això.

 





