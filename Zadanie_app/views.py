from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from Zadanie_app.models import File
from django.urls import reverse_lazy
from django.urls import reverse
from Zadanie_app.data_analizing import DataAnalizing
from Zadanie_app.forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class FileListView(LoginRequiredMixin, ListView):
    template_name = 'file/files_list.html'

    def get_queryset(self):
        user = self.request.user
        files = File.objects.filter(user=user)
        return files


class FileDetailView(LoginRequiredMixin, DetailView):
    model = File
    template_name = 'file/file_detail.html'

    def get_context_data(self, **kwargs):
        context = super(FileDetailView, self).get_context_data(**kwargs)
        context = context | DataAnalizing(self.object).get_data()

        return context


class FileCreateView(LoginRequiredMixin, CreateView):
    model = File
    fields = ['file']
    template_name = 'file/file_create.html'

    def form_valid(self, form):

        if form.is_valid():

            file_path = f"user_{self.request.user.id}/{form.cleaned_data['file']}/{form.cleaned_data['file']}"

            if File.objects.filter(file=file_path).exists():
                form.add_error('file', 'Posiadasz już plik o takiej nazwie')
                return self.form_invalid(form)

            file = form.save(commit=False)
            file.user = self.request.user
            file.save()

            return redirect(reverse('files_list'))
        return HttpResponse(status=404)


class FileDeleteView(LoginRequiredMixin, DeleteView):
    model = File
    success_url = reverse_lazy('files_list')



