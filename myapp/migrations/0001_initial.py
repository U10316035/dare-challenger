# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='challengeData',
            fields=[
                ('urlnumber', models.AutoField(serialize=False, primary_key=True)),
                ('urlnum', models.CharField(default='', max_length=20)),
                ('username', models.CharField(default='', max_length=20)),
                ('title', models.CharField(default='', max_length=20)),
                ('detail', models.TextField(default='', max_length=200, null=True)),
                ('stTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('endTime', models.CharField(default='', max_length=50)),
                ('mancount', models.PositiveIntegerField(default=0)),
                ('permission', models.CharField(default='', max_length=50)),
                ('joincount', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('urlnumber', models.CharField(default='', max_length=20)),
                ('username', models.CharField(default='', max_length=20)),
                ('title', models.CharField(default='', max_length=20)),
                ('detail', models.CharField(default='', max_length=200)),
                ('video', models.CharField(default='', max_length=300)),
                ('startTime', models.CharField(default='', max_length=50)),
                ('endTime', models.CharField(default='', max_length=50)),
                ('mancount', models.PositiveIntegerField(default=0)),
                ('isFinish', models.BooleanField(default=False)),
                ('videopic', models.CharField(default='', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='detailResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('urlnumber', models.CharField(default='', max_length=20)),
                ('username', models.CharField(default='', max_length=20)),
                ('response', models.CharField(default='', max_length=100)),
                ('postTime', models.CharField(default='', max_length=20)),
                ('detailowner', models.CharField(default='', max_length=20)),
                ('whichDetail', models.ForeignKey(to='myapp.detail')),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(default='', max_length=20)),
                ('password', models.CharField(default='', max_length=30)),
                ('email', models.EmailField(default='', max_length=100)),
            ],
        ),
    ]
