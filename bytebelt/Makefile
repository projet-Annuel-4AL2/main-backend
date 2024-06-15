PYTHON_FILES := $(wildcard *.py)
HTML_FILES := $(wildcard *.html)

.PHONY: clean

clean:
	@echo "Nettoyage des fichiers Python..."
	@autopep8 --in-place --recursive $(PYTHON_FILES)
	@echo "Nettoyage des fichiers HTML..."
	@python clean_html.py $(HTML_FILES)
	@echo "Nettoyage terminé."

python-shell:
	@CONTAINER_ID=$$(docker ps -qf "ancestor=bytebelt-web") && \
	docker exec -it $$CONTAINER_ID /bin/bash


postgres-shell:
	@CONTAINER_ID=$$(docker ps -qf "ancestor= postgres:latest") && \
	docker exec -it $$CONTAINER_ID psql -U bytebelt -d bytebelt

postgres-user-test:
	@CONTAINER_ID=$$(docker ps -qf "ancestor= postgres:latest") && \
	docker exec -it $$CONTAINER_ID psql -U bytebelt -d bytebelt -c "INSERT INTO \"userApi_customuser\" ( id , is_active,is_staff ,is_superuser, first_name , last_name ,username, password, email , role , date_joined , created_at ,updated_at ) VALUES (  'cbd45656-bfb7-3275-8c1c-7ab8aa6ee487', true , true , true, 'gavin' ,'gavin' ,'testuser', 'testpassword', 'testuser@example.com' , 'admin','2021-09-01 00:00:00' , '2021-09-01 00:00:00' , '2021-09-01 00:00:00' )"

migration-user-api:
	@CONTAINER_ID=$$(docker ps -qf "ancestor=bytebelt-web") && \
	docker exec -it $$CONTAINER_ID python3 manage.py makemigrations userApi && \
	docker exec -it $$CONTAINER_ID python3 manage.py migrate userApi

migration:
	@CONTAINER_ID=$$(docker ps -qf "ancestor=bytebelt-web") && \
	docker exec -it $$CONTAINER_ID python3 manage.py makemigrations && \
	docker exec -it $$CONTAINER_ID python3 manage.py migrate

migrate:
	@CONTAINER_ID=$$(docker ps -qf "ancestor=bytebelt-web") && \
	docker exec -it $$CONTAINER_ID python3 manage.py migrate

postgres-tables:
	@CONTAINER_ID=$$(docker ps -qf "ancestor= postgres:latest") && \
	docker exec -it $$CONTAINER_ID psql -U bytebelt -d bytebelt -c "\dt"

postgres-show-users:
	@CONTAINER_ID=$$(docker ps -qf "ancestor= postgres:latest") && \
    docker exec -it $$CONTAINER_ID psql -U bytebelt -d bytebelt -c "SELECT * FROM \"userApi_customuser\""

postgres-users-colonnes:
	@CONTAINER_ID=$$(docker ps -qf "ancestor= postgres:latest") && \
	docker exec -it $$CONTAINER_ID psql -U bytebelt -d bytebelt -c "\d \"userApi_customuser\""

superuser:
	@CONTAINER_ID=$$(docker ps -qf "ancestor=bytebelt-web") && \
	docker exec -it $$CONTAINER_ID python3 manage.py createsuperuser

python-collectstatic:
	@CONTAINER_ID=$$(docker ps -qf "ancestor=bytebelt-web") && \
	docker exec -it $$CONTAINER_ID python3 manage.py collectstatic  


help:
	@echo "\033[0;32m clean \033[0m : Nettoie les fichiers Python et HTML."
	@echo "\033[0;32m python-shell \033[0m : Ouvre un shell Python dans le conteneur Docker."
	@echo "\033[0;32m postgres-shell \033[0m : Ouvre un shell PostgreSQL dans le conteneur Docker."
	@echo "\033[0;32m postgres-user-test \033[0m : Ajoute un utilisateur de test dans la base de données PostgreSQL."
	@echo "\033[0;32m migration-user-api \033[0m : Crée les migrations pour l'application userApi et les executes."
	@echo "\033[0;32m postgres-tables \033[0m : Affiche les tables de la base de données PostgreSQL."
	@echo "\033[0;32m postgres-show-users \033[0m : Affiche les utilisateurs de la base de données PostgreSQL."
	@echo "\033[0;32m python-superuser \033[0m : Crée un superutilisateur pour l'application Django."
	@echo "\033[0;32m help \033[0m : Affiche ce message d'aide."

