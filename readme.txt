python manage.py makemigrations counter
python manage.py migrate counter
pip install daphne


# mysite/settings.py
INSTALLED_APPS = [
    'daphne',

# eof
ASGI_APPLICATION = "mysite.asgi.application"

python3 -m pip install channels_redis