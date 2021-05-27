from django.contrib import admin
from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('file',)}
