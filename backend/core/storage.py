# -*- coding: utf-8 -*-
from django.core.files.storage import FileSystemStorage


class FileSystemOverwriteStorage(FileSystemStorage):
    """
    Custom file system storage
    Overwrite get_available_name to make Django replace files instead of
    creating new ones over and over again.
    """

    def get_available_name(self, name: str, max_length=None):
        self.delete(name)
        return super().get_available_name(name, max_length)
