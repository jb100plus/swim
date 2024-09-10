# swim

fürs 24 h Schwimmen

immer als normaler Benutzer ausführen,
wenn sudo, landen die schlüssel nicht an der richtigen Stelle -> dann immer sudo :-(

* ssh-keygen -t ed25519 -C "jb.100plus@gmx.de"
* eval "$(ssh-agent -s)"
* ssh-add ~/.ssh/gh240910
* ssh -T git@ssh.github.com -p 443
* git clone ssh://git@ssh.github.com:443/jb100plus/swim
* git add
* git commit
* git push

1. rename swim to counter
2. django-admin startproject mysite
3. create a base dir
4. create a virtual environment: python3 -m venv ./venv
5. pip install djangopip install daphne
6. pip install channels_redis
7. pip install apscheduler
8. in settings.py  INSTALLED_APPS=  ['daphne',  'counter',  
am Ende:

ASGI_APPLICATION = "mysite.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

mysite/urls.py
urlpatterns = [
    path("", include("counter.urls")),
    path('admin/', admin.site.urls),
]

python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate

docker run --rm -p 6379:6379 redis:7

