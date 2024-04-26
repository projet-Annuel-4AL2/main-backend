# Main-project
Install django 
pyenv install 3.12.1

python3 -m venv env
source env/bin/activate
python -m pip install django

python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt

https://realpython.com/django-setup/