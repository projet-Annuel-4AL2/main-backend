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

postgres-tables:
	@CONTAINER_ID=$$(docker ps -qf "ancestor= postgres:latest") && \
	docker exec -it $$CONTAINER_ID psql -U bytebelt -d bytebelt -c "\dt"

postgres-show-users:
	@CONTAINER_ID=$$(docker ps -qf "ancestor= postgres:latest") && \
    docker exec -it $$CONTAINER_ID psql -U bytebelt -d bytebelt -c "SELECT * FROM \"userApi_customuser\""