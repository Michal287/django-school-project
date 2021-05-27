from django.db.models.signals import post_save
from Zadanie_app.models import File
from Zadanie_app.data_analizing import DataAnalizing


def data_analizing_signal(sender, instance, created, **kwargs):
    DataAnalizing(instance).save()


post_save.connect(data_analizing_signal, sender=File)