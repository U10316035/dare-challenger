# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20170107_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengedata',
            name='endTime',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
