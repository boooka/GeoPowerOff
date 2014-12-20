# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GeoParse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressEnum',
            fields=[
                ('adress_enum_id', models.AutoField(serialize=False, primary_key=True)),
                ('street', models.TextField(verbose_name='\u0410\u0434\u0440\u0435\u0441')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AddressEnumMap',
            fields=[
                ('address_enum_map_id', models.AutoField(serialize=False, primary_key=True)),
                ('address_enum', models.ForeignKey(to='GeoParse.AddressEnum')),
                ('place', models.ForeignKey(to='GeoParse.MyMap')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AddressMatches',
            fields=[
                ('address_matches_id', models.AutoField(serialize=False, primary_key=True)),
                ('map_engine', models.CharField(default=b'yandex', max_length=10, choices=[(b'yandex', b'\xd0\xaf\xd0\xbd\xd0\xb4\xd0\xb5\xd0\xba\xd1\x81'), (b'google', b'Google')])),
                ('address', models.CharField(max_length=255, verbose_name='\u041f\u043b\u043e\u0445\u043e\u0439 \u0430\u0434\u0440\u0435\u0441')),
                ('address_matches', models.CharField(max_length=255, verbose_name='\u0410\u0434\u0440\u0435\u0441')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AddressPowerOutage',
            fields=[
                ('address_power_outage_id', models.AutoField(serialize=False, primary_key=True)),
                ('address_enum', models.ForeignKey(to='GeoParse.AddressEnum')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OutageReason',
            fields=[
                ('outagereason_id', models.AutoField(serialize=False, primary_key=True)),
                ('reason', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PowerObject',
            fields=[
                ('power_object_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041e\u0431\u044a\u0435\u043a\u0442 \u043e\u0431\u0441\u043b\u0443\u0436\u0438\u0432\u0430\u043d\u0438\u044f')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PowerOutage',
            fields=[
                ('power_outage_id', models.AutoField(serialize=False, primary_key=True)),
                ('date_from', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0442\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f')),
                ('date_to', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0432\u043e\u0437\u043e\u0431\u043d\u043e\u043b\u0435\u043d\u0438\u044f')),
                ('description', models.TextField()),
                ('address_representation', models.TextField(verbose_name='\u041f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0430\u0434\u0440\u0435\u0441\u0430')),
                ('outage_reason', models.ForeignKey(to='GeoParse.OutageReason')),
                ('power_object', models.ForeignKey(to='GeoParse.PowerObject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='addresspoweroutage',
            name='power_outage',
            field=models.ForeignKey(to='GeoParse.PowerOutage'),
            preserve_default=True,
        ),
    ]
