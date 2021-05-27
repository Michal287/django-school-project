from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
import pandas as pd


def file_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}/{filename}'


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=file_directory_path, storage=False)
    slug = models.SlugField(max_length=200)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.file.name)
        super(File, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('file_detail', args=[self.id, self.slug])

    def get_name(self):
        return self.file.name.split('/', 1)[1]

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
    min_value = models.FloatField()
    max_value = models.FloatField()
    mean = models.FloatField()
    median = models.FloatField()
    std = models.FloatField()


class FileObjects(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    unique_values = models.IntegerField()
    empty_values = models.IntegerField()
    nan_values = models.IntegerField()


class FileDateTime(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    first_date = models.DateField()
    last_date = models.DateField()


class FileHistogram(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    image = models.ImageField(max_length=255, blank=True)