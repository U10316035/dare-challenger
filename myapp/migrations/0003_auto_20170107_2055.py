# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20170107_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengedata',
            name='endTime',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
