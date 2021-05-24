This repository is a boilerplate Django project for quickly getting started.

Steps:

1. Clone/pull/download this repository
2. Create a virtualenv with `virtualenv env` and install dependencies with `pip install -r requirements.txt`
3. Configure your .env variables
4. Rename your project with `python manage.py rename <yourprojectname> <newprojectname>`


1- in linux


install python3 virtualenv pip
 
virtualenv -p python3 .venv

source .venv/bin/activate

pip install -r requirements.txt

./manage.py makemigrations

./manage.py migrate

./manage.py runserver

./manage.py createsuperuser



	
