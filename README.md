# AutoApplyDjando
Django Backend Easy Auto Apply App




# For developers
create django project, create an app inside
``````
django-admin startproject <project_name>
cd <project_name>
python manage.py startapp <app_name>
``````
run the server
``````
python manage.py runserver 0.0.0.0:8000
``````
for testing, add allowed hosts as configured.

apply migrations to database:
``````
python manage.py makemigrations
python manage.py migrate
``````