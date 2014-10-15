# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_building_neighbourhood'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='neighbourhood',
            field=models.CharField(default=b'None', max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
