# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from yandex_maps.models import get_static_map_url
from yandex_maps import api
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis import models as gis_models


class LocatonDevision(models.Model):
    '''
    Список региональных ведомств
    '''
    class Meta:
        abstract = True

    name = models.CharField(_(u'Название'), max_length=255, blank=False)
    #view = models.CharField(_(u'Представление'), max_length=255)
    url = models.URLField(blank=False)

    def __unicode__(self):
        return self.name

class Area(LocatonDevision):
    class Meta:
        verbose_name = _(u'Область')
        verbose_name_plural = _(u'Области')

class District(LocatonDevision):
    class Meta:
        verbose_name = _(u'Район')
        verbose_name_plural = _(u'Районы')

    area = models.ForeignKey(Area)

class AddressOnMap(models.Model):
    address = models.CharField(_(u"Адрес"), max_length=255, blank=True, db_index=True)
    longitude = models.FloatField(_(u"Долгота"), null=True, blank=True)
    latitude = models.FloatField(_(u"Широта"), null=True, blank=True)

    @staticmethod
    def get_detail_level(self):
        return 5

    def get_map_url(self, width=None, height=None, detail_level=5):
        if settings.YANDEX_MAPS_API is None:
            return ""
        return get_static_map_url(self.longitude, self.latitude, width, height, detail_level)

    def get_external_map_url(self, detail_level=14):
        return api.get_external_map_url(self.longitude, self.latitude, detail_level)

    def fill_geocode_data(self):
        if settings.YANDEX_MAPS_API is not None:
            self.longitude, self.latitude = api.geocode(settings.YANDEX_MAPS_API_KEY, self.address)

    def save(self, *args, **kwargs):
        # fill geocode data if it is unknown
        if self.pk or (self.longitude is None) or (self.latitude is None):
            self.fill_geocode_data()
        super(AddressOnMap, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.address


class OutageReason(models.Model):
    '''
    Причины отключения
    '''
    reason = models.CharField(_(u"Причина"), max_length=255, blank=False, db_index=True, unique=True)

    def __unicode__(self):
        return self.reason

class PowerObject(models.Model):
    '''
    Объекты обслуживания
    '''
    outageobject = models.CharField(_(u"Объект обслуживания"), max_length=255, blank=False, db_index=True, unique=True)

    def __unicode__(self):
        return self.outageobject

class PowerOutage(models.Model):
    '''
    Отключения
    '''
    power_outage_id = models.AutoField(primary_key=True)
    power_object = models.ForeignKey(PowerObject, verbose_name=_(u"объект обслуживания"))
    outage_reason = models.ForeignKey(OutageReason, verbose_name=_(u"причина"))
    district = models.ForeignKey(District, verbose_name=_(u'район'))
    date_from = models.DateTimeField(_(u"Дата отключения"), auto_now=False, blank=False)
    date_to = models.DateTimeField(_(u"Дата возобноления"), auto_now=False, blank=False)
    description = models.TextField(_(u"Описание"))
    address_representation = models.TextField(_(u"Представление адреса"))
    outage_type = models.CharField(max_length=10, choices=(
        ('emergency', _(u"Аварийное")),
        ('planed', _(u"Плановое")),
    ), default='planed')

    def __unicode__(self):
        return u"[%s <%s, %s: %s - %s>]" % (
            self.power_outage_id,
            self.power_object,
            self.outage_reason,
            self.date_from, self.date_to
        )

class AddressEnum(models.Model):
    '''
    Определение набора адрессов (одной улицы)
    '''
    adress_enum_id = models.AutoField(primary_key=True)
    # Часть адреса из отключения, со списком домов, расположенных на одной улице
    district = models.ForeignKey(District)
    street = models.TextField(_(u"Адрес"), unique=True)

    def get_full(self):
        return u'%s, %s, %s' % (self.district.area, self.district, self.street)

    def __unicode__(self):
        return self.street

class AddressEnumMap(models.Model):
    '''
    Координаты адрессов
    '''
    address_enum_map_id = models.AutoField(primary_key=True)
    address_enum = models.ForeignKey(AddressEnum, verbose_name=_(u"опредение адреса"), db_index=True)
    place = models.ForeignKey(AddressOnMap, verbose_name=_(u"координата"))

    def save(self, *args, **kwargs):
        super(AddressEnumMap, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.address_enum

class AddressPowerOutage(models.Model):
    '''
    Группы адресов отключений
    '''
    address_power_outage_id = models.AutoField(primary_key=True)
    power_outage = models.ForeignKey(PowerOutage, verbose_name=_(u"отключение"))
    address_enum = models.ForeignKey(AddressEnum, verbose_name=_(u"по списку адресов"))


class AddressMatches(models.Model):
    '''
    "Плохие" адреса
    '''
    address_matches_id = models.AutoField(primary_key=True)
    map_engine = models.CharField(max_length=10, choices=(
        ('yandex', _(u"Яндекс")),
        ('google', _(u"Google")),
    ), default='yandex')
    address = models.CharField(_(u"Плохой адрес"), max_length=255, db_index=True)
    address_matches = models.CharField(_(u"Адрес"), max_length=255, db_index=True)

