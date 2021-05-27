from django.forms import ModelForm
from django.core.exceptions import ValidationError
from Zadanie_app.models import File


class FileCreateForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']

    def clean(self):
        cleaned_data = super(FileCreateForm, self).clean()

        file = cleaned_data.get('file')

        if File.objects.get(file=file, user=self.request.user) is not None:
            raise ValidationError(("Posiadasz już plik o takiej nazwie"))

        return cleaned_data
