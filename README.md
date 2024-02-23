add db_dump.sql to postgres filder

docker compose up --build

cd test_project
poetry shell

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
