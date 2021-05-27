from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from Zadanie_app.models import File
from django.urls import reverse_lazy
from Zadanie_app.Read_csv import DataAnalizing
from django.urls import reverse


class FileListView(LoginRequiredMixin, ListView):
    template_name = 'files_list.html'

    def get_queryset(self):
        user = self.request.user
        files = File.objects.filter(user=user)
        return files


class FileDetailView(LoginRequiredMixin, DetailView):
    model = File
    template_name = 'file_detail.html'


class FileCreateView(LoginRequiredMixin, CreateView):
    model = File
    fields = ['file']
    template_name = 'file_create.html'

    def form_valid(self, form):

        file_name = f"user_{self.request.user.id}/{form.cleaned_data['file']}"

        if File.objects.filter(file=file_name).exists():
            form.add_error('file', 'Posiadasz już plik o takiej nazwie')
            return self.form_invalid(form)

        if form.is_valid():
            file = form.save(commit=False)
            file.user = self.request.user
            file.save()

            f = DataAnalizing(file, self.request.user)
            f.save()

            return redirect(reverse('files_list'))
        return HttpResponse(status=404)


class FileDeleteView(LoginRequiredMixin, DeleteView):
    model = File
    success_url = reverse_lazy('files_list')



