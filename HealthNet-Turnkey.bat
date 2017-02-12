unzip Healthnet.zip
cd Healthnet/healthnetproject
python manage.py makemigrations
python manage.py migrate
python add_records.py
start "" http://localhost:8000/
python manage.py runserver
