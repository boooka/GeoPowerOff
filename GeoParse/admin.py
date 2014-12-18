from django.contrib import admin
from yandex_maps.models import MapAndAddress

admin.site.register([MapAndAddress,])

admin.autodiscover()

# Register your models here.
