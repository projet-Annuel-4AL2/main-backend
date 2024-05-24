PYTHON_FILES := $(wildcard *.py)
HTML_FILES := $(wildcard *.html)


.PHONY: clean

clean:
	@echo "Nettoyage des fichiers Python..."
	@autopep8 --in-place --recursive $(PYTHON_FILES)
	@echo "Nettoyage des fichiers HTML..."
	@python clean_html.py $(HTML_FILES)
	@echo "Nettoyage terminé."


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