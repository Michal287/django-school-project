import pandas as pd
from django.core.files.images import ImageFile
from Zadanie_app.models import FileNumerics, FileObjects, FileDateTime, FileHistogram
from pandas.api.types import is_numeric_dtype, is_object_dtype, is_bool_dtype, is_categorical_dtype
import matplotlib.pyplot as plt
from io import BytesIO


class DataAnalizing:
    def __init__(self, file):
        self.file = file
        self.df = pd.read_csv(file.file, delimiter=';', keep_default_na=False)

    def create_hist(self, col):

        virtual_box = BytesIO()

        self.df[col].plot.bar(rot=0, alpha=0.5)

        plt.savefig(virtual_box, format="png")
        image = ImageFile(virtual_box)

        model_instance = FileHistogram(file=self.file, column=col, image=image)

        model_instance.image.save(f'{self.file.dir_path()}/histograms/{col}.png', image)
        model_instance.save()

        return True

    def numerics_save(self, col):
        return FileNumerics.objects.create(file=self.file,
                                           column=col,
                                           min_value=self.df[col].min(),
                                           max_value=self.df[col].max(),
                                           mean=self.df[col].mean(),
                                           median=self.df[col].median(),
                                           std=self.df[col].std())

    def object_save(self, col):
        empty_values = (self.df[col] == '').sum()
        return FileObjects.objects.create(file=self.file,
                                          column=col,
                                          unique_values=(self.df[col].nunique())-empty_values,
                                          empty_values=empty_values,
                                          nan_values=(self.df[col] == 'NaN').sum())

    def date_save(self, col):
        return FileDateTime.objects.create(file=self.file,
                                           column=col,
                                           first_date=self.df[col].min(),
                                           last_date=self.df[col].max())

    def save(self):

        for col in self.df.columns:

            if is_numeric_dtype(self.df[col]):
                if col != "id":
                    self.numerics_save(col)

            if is_object_dtype(self.df[col]):

                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                    self.date_save(col)

                except ValueError:
                    self.object_save(col)

            if is_numeric_dtype(self.df[col]) or is_bool_dtype(self.df[col]) or is_categorical_dtype(self.df[col]):
                if col != "id":
                    self.create_hist(col)

    def get_data(self):
        return {"datetime": FileDateTime.objects.filter(file=self.file),
                "numerics": FileNumerics.objects.filter(file=self.file),
                "objects": FileObjects.objects.filter(file=self.file),
                "historams": FileHistogram.objects.filter(file=self.file)}
