# Generated by Django 3.0 on 2023-12-19 19:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TT_tele_calibration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FEB_ID', models.IntegerField()),
                ('cat_ID', models.IntegerField()),
                ('CH', models.IntegerField()),
                ('a0', models.FloatField()),
                ('a00', models.FloatField()),
                ('a1', models.FloatField()),
                ('a2', models.FloatField()),
                ('a3', models.FloatField()),
                ('a4', models.FloatField()),
                ('a5', models.FloatField()),
                ('b', models.FloatField()),
                ('ChiSq', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('emailaddress', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=255)),
                ('ctime', models.DateTimeField(default=datetime.datetime.now)),
                ('mtime', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
