import pandas as pd
from django.core.files.images import ImageFile
from Zadanie_app.models import FileNumerics, FileObjects, FileDateTime, FileHistogram
from pandas.api.types import is_numeric_dtype, is_object_dtype, is_bool_dtype, is_categorical_dtype
import matplotlib.pyplot as plt
from io import BytesIO


def create_hist(df, col, file, user):

    virtual_box = BytesIO()

    df[col].hist(bins=12, alpha=0.5)

    plt.savefig(virtual_box, format="png")
    image = ImageFile(virtual_box)

    model_instance = FileHistogram(file=file, image=image)
    model_instance.image.save(f'user_{user.id}/histograms/{col}.png', image)
    model_instance.save()

    return True


def numerics_save(df, col, file):
    return FileNumerics.objects.create(file=file,
                                       min_value=df[col].min(),
                                       max_value=df[col].max(),
                                       mean=df[col].mean(),
                                       median=df[col].median(),
                                       std=df[col].std())


def object_save(df, col, file):
    return FileObjects.objects.create(file=file,
                                      unique_values=df[col].nunique(),
                                      empty_values=(df[col] == '').sum(),
                                      nan_values=(df[col] == 'NaN').sum())


def date_save(df, col, file):
    return FileDateTime.objects.create(file=file,
                                       first_date=df[col].min(),
                                       last_date=df[col].max())


class DataAnalizing:
    def __init__(self, file, user):
        self.file = file
        self.df = pd.read_csv(file.file, delimiter=';', keep_default_na=False)
        self.user = user

    def save(self):

        for col in self.df.columns:

            if is_numeric_dtype(self.df[col]):
                numerics_save(self.df, col, self.file)

            if is_object_dtype(self.df[col]):

                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                    date_save(self.df, col, self.file)

                except ValueError:
                    object_save(self.df, col, self.file)

            if is_numeric_dtype(self.df[col]) or is_bool_dtype(self.df[col]) or is_categorical_dtype(self.df[col]):
                create_hist(self.df, col, self.file, self.user)
