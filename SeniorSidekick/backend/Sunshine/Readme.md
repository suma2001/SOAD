## Before running the following code, do the following - 

#### 1. Delete all the tables from the postgres database
  - DROP SCHEMA public CASCADE;
  - CREATE SCHEMA public;
  
#### 2. Delete all migrations in the *migration* folder.

#### 3. Then run the following :
  - python manage.py makemigrations
  - python manage.py migrate
  - python manage.py runserver
