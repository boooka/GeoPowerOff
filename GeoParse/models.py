# -*- coding: utf-8 -*-
from django.db import models
from yandex_maps.models import MapAndAddress
from django.utils.translation import ugettext_lazy as _

class MyMap(MapAndAddress):
    pass

class OutageReason(models.Model):
    '''
    Причины отключения
    '''
    outagereason_id = models.AutoField(primary_key=True)
    reason = models.TextField()

class PowerObject(models.Model):
    '''
    Объекты обслуживания
    '''
    power_object_id = models.AutoField(primary_key=True)
    name = models.CharField(_(u"Объект обслуживания"), max_length=255)

class PowerOutage(models.Model):
    '''
    Отключения
    '''
    power_outage_id = models.AutoField(primary_key=True)
    power_object = models.ForeignKey(PowerObject, verbose_name=_(u"объект обслуживания"))
    outage_reason = models.ForeignKey(OutageReason, verbose_name=_(u"причина"))
    date_from = models.DateTimeField(_(u"Дата отключения"), auto_now=False)
    date_to = models.DateTimeField(_(u"Дата возобноления"), auto_now=False)
    description = models.TextField(_(u"Описание"))
    address_representation = models.TextField(_(u"Представление адреса"))

class AddressEnum(models.Model):
    '''
    Определение набора адрессов (одной улицы)
    '''
    adress_enum_id = models.AutoField(primary_key=True)
    # Часть адреса из отключения, со списком домов, расположенных на одной улице
    street = models.TextField(_(u"Адрес"))

class AddressEnumMap(models.Model):
    '''
    Координаты адрессов
    '''
    address_enum_map_id = models.AutoField(primary_key=True)
    address_enum = models.ForeignKey(AddressEnum, verbose_name=_(u"опредение адреса"))
    place = models.ForeignKey(MyMap, verbose_name=_(u"координата"))

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
        ('yandex', 'Яндекс'),
        ('google', 'Google'),
    ), default='yandex')
    address = models.CharField(_(u"Плохой адрес"), max_length=255)
    address_matches = models.CharField(_(u"Адрес"), max_length=255)