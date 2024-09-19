from django.contrib import admin
from .models import Starter, Log, LastLog
 
# registering the model
# admin.site.register(Starter)
admin.site.register(Log)
admin.site.register(LastLog)

from import_export.admin import ImportExportModelAdmin
from import_export import resources

class StarterResource(resources.ModelResource):
    class Meta:
        model = Starter

class StarterAdmin(ImportExportModelAdmin):
    resource_classes = [StarterResource]

admin.site.register(Starter, StarterAdmin)