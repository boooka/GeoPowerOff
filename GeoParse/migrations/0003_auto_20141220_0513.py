# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GeoParse', '0002_auto_20141220_0429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressenummap',
            name='address_enum',
            field=models.ForeignKey(verbose_name='\u043e\u043f\u0440\u0435\u0434\u0435\u043d\u0438\u0435 \u0430\u0434\u0440\u0435\u0441\u0430', to='GeoParse.AddressEnum'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='addressenummap',
            name='place',
            field=models.ForeignKey(verbose_name='\u043a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u0430', to='GeoParse.MyMap'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='addresspoweroutage',
            name='address_enum',
            field=models.ForeignKey(verbose_name='\u043f\u043e \u0441\u043f\u0438\u0441\u043a\u0443 \u0430\u0434\u0440\u0435\u0441\u043e\u0432', to='GeoParse.AddressEnum'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='addresspoweroutage',
            name='power_outage',
            field=models.ForeignKey(verbose_name='\u043e\u0442\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435', to='GeoParse.PowerOutage'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='poweroutage',
            name='description',
            field=models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='poweroutage',
            name='outage_reason',
            field=models.ForeignKey(verbose_name='\u043f\u0440\u0438\u0447\u0438\u043d\u0430', to='GeoParse.OutageReason'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='poweroutage',
            name='power_object',
            field=models.ForeignKey(verbose_name='\u043e\u0431\u044a\u0435\u043a\u0442 \u043e\u0431\u0441\u043b\u0443\u0436\u0438\u0432\u0430\u043d\u0438\u044f', to='GeoParse.PowerObject'),
            preserve_default=True,
        ),
    ]
