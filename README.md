# ByteBelt
Install django 
pyenv install 3.12.1

python3 -m venv myvenv
source myvenv/bin/activate
python -m pip install django

python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt. /// firebase-admin
pip install autopep8 beautifulsoup4

https://realpython.com/django-setup/

Exulter dans une sandbox 
Un docker avec un worker avec un redis 
Sur un kube 



 # Set up the database && apres un ajout de model pour mettre a jour la base de donnee et toujours les executer dans le container docker
python manage.py makemigrations
python manage.py migrate

#set up userApi
pip install djangorestframework


#superuser already created ou utiliser la make file
Username: aude
email: audesandrine6@gmail.com
Password: aude

#pour les fichiers static on a besoin de les collecter  avec la commande suivante

make python-collectstatic

#afficher tous les modules installés
pip freeze
asgiref==3.8.1
beautifulsoup4==4.12.3
Django==4.2.13
django-bootstrap-v5==1.0.11
soupsieve==2.5
sqlparse==0.5.0