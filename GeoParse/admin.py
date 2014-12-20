from django.contrib import admin
from django.apps import apps

admin.site.register([i for i in apps.get_models() if i not in admin.site._registry])

admin.autodiscover()

# Register your models here.
