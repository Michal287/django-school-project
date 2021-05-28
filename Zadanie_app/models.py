import shutil
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
import pandas as pd
import os


def file_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}/{filename}'


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_directory_path, storage=False)
    slug = models.SlugField(max_length=200)

    _metadata = {
        'lines': 'get_df_lines',
    }

    def filename(self):
        return (str(self.file.name).split("/"))[-1:][0]

    def get_df_lines(self):
        df = pd.read_csv(self.file, delimiter=';')
        return len(df)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.file.name)
        super(File, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('file_detail', args=[self.id, self.slug])

    def dir_path(self):
        return "/".join(str(self.file).split("/")[:-1])

    def delete(self):
        path = settings.MEDIA_ROOT + self.dir_path()

        if os.path.exists(path):
            shutil.rmtree(path)

        return super(File, self).delete()

    def clean(self):
        if not self.file.name.endswith('.csv'):
            raise ValidationError(("Plik nie jest plikiem CSV"))

        df = pd.read_csv(self.file, delimiter=';')

        if len(df.columns) > 20:
            raise ValidationError(("Plik ma za dużo kolumn"))

        if len(df) > 1000:
            raise ValidationError(("Plik ma za dużo rekordów"))


class FileNumerics(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    column = models.CharField(max_length=128)
    col_type = models.CharField(max_length=32)
    min_value = models.FloatField()
    max_value = models.FloatField()
    mean = models.FloatField()
    median = models.FloatField()
    std = models.FloatField()


class FileObjects(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    column = models.CharField(max_length=128)
    col_type = models.CharField(max_length=32)
    unique_values = models.IntegerField()
    empty_values = models.IntegerField()
    nan_values = models.IntegerField()


class FileDateTime(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    column = models.CharField(max_length=128)
    col_type = models.CharField(max_length=32)
    first_date = models.DateField()
    last_date = models.DateField()


class FileHistogram(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    column = models.CharField(max_length=128)
    col_type = models.CharField(max_length=32)
    image = models.ImageField(max_length=255, blank=True)
