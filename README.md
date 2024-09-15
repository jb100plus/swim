# swim

fürs 24 h Schwimmen

immer als normaler Benutzer ausführen,
wenn sudo, landen die schlüssel nicht an der richtigen Stelle -> dann immer sudo :-(

* ssh-keygen -t ed25519 -C "jb.100plus..."
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
5. pip install django
6. pip install daphne
7. pip install channels_redis
8. pip install apscheduler
9. pip install django-import-export
10. in settings.py  INSTALLED_APPS=  ['daphne',  'counter',  'import_export',

for django_import-export:
 python manage.py collectstatic

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

asgi.py:
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

from counter.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)

python manage.py createsuperuser
python manage.py makemigrations counter
python manage.py migrate

docker run --rm -p 6379:6379 redis:7

