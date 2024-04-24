from django.contrib import admin
from .models import Starter, Log, LastLog, ListHash
 
# registering the model
admin.site.register(Starter)
admin.site.register(Log)
admin.site.register(LastLog)
admin.site.register(ListHash)