# Generated by Django 3.2 on 2021-05-11 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zadanie_app', '0002_auto_20210511_1917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filenumerics',
            name='type',
        ),
    ]
