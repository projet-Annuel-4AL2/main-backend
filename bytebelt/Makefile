PYTHON_FILES := $(wildcard *.py)
HTML_FILES := $(wildcard *.html)

.PHONY: clean

clean:
	@echo "Nettoyage des fichiers Python..."
	@autopep8 --in-place --recursive $(PYTHON_FILES)
	@echo "Nettoyage des fichiers HTML..."
	@python clean_html.py $(HTML_FILES)
	@echo "Nettoyage terminé."
