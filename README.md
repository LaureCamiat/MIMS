# MIMS Programmation Project - Laure CAMIAT

Pour lancer l'application, il est nécessaire d'avoir installé Python et pip au préalable. Une fois que vous êtes dans le répertoire "MIMS", écrire en ligne de commandes les instructions suivantes :

MIMS> pip install virtualenv virtualenvwrapper-win flask_sqlalchemy
MIMS> mkvirtualenv CrawlApp

(CrawlApp)> pipenv install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy lxml requests
(CrawlApp)> python
>>> from app import db
>>> db.create_all()
>>> exit()
(CrawlApp)> py app.py


Une fois que toutes ces actions sont réalisées, le lancement du crawling d'image s'effectue avec la commande suivante :

$ curl -X POST http://localhost:8080?threads=nb_thread -H "Content-Type: application/json" --data {\"urls\":[\"url1\",\"url2\",...]}

(où nb_thread est le nombre de thread que vous voulez utiliser et url1, url2, etc... sont les urls dont vous voulez collecter les images)


Pour effectuer le suivi d'un job_id et récupérer toutes les images collectées, lancer :

$ curl -X GET http://localhost:8080/status/job_id

(où job_id est la chaîne de charactère renvoyée à la première commande pour identifier le crawl)



