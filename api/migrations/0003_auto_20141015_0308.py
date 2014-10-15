# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20141009_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='neighbourhood',
            field=models.CharField(default=None, max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='bedB',
            field=models.CharField(max_length=80, blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='bedC',
            field=models.CharField(max_length=80, blank=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='bedD',
            field=models.CharField(max_length=80, blank=True),
        ),
    ]
