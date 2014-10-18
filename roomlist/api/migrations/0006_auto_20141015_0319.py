# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_building_neighbourhood'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='neighbourhood',
            field=models.CharField(default=b'NA', max_length=100, choices=[(b'NA', b'None'), (b'AQ', b'Aquia'), (b'RA', b'Rappahannock'), (b'SH', b'Shenandoah')]),
        ),
    ]
