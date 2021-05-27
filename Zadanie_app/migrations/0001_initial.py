# Generated by Django 3.2 on 2021-05-27 23:18

import Zadanie_app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=Zadanie_app.models.file_directory_path)),
                ('slug', models.SlugField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileObjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_values', models.IntegerField()),
                ('empty_values', models.IntegerField()),
                ('nan_values', models.IntegerField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Zadanie_app.file')),
            ],
        ),
        migrations.CreateModel(
            name='FileNumerics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_value', models.FloatField()),
                ('max_value', models.FloatField()),
                ('mean', models.FloatField()),
                ('median', models.FloatField()),
                ('std', models.FloatField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Zadanie_app.file')),
            ],
        ),
        migrations.CreateModel(
            name='FileHistogram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=255, upload_to='')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Zadanie_app.file')),
            ],
        ),
        migrations.CreateModel(
            name='FileDateTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_date', models.DateField()),
                ('last_date', models.DateField()),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Zadanie_app.file')),
            ],
        ),
    ]
