# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20141015_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='neighbourhood',
            field=models.CharField(default=b'na', max_length=100, choices=[(b'na', b'None'), (b'aq', b'Aquia'), (b'ra', b'Rappahannock'), (b'sh', b'Shenandoah')]),
        ),
    ]
