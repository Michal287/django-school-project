from django.core.files.storage import FileSystemStorage


class FileIncrementRename(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        return name
