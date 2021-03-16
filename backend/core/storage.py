import os
from django.core.files.storage import FileSystemStorage
from django.utils.functional import cached_property
from django.conf import settings


class OverwriteStorage(FileSystemStorage):

    @cached_property
    def base_url(self):
        if self._base_url is not None and not self._base_url.endswith('/'):
            self._base_url += '/'
        return self._value_or_setting(self._base_url, settings.STATIC_URL)

    def get_available_name(self, name, *args, **kwargs):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        Found at http://djangosnippets.org/snippets/976/
        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):
        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name) and os.path.exists(
                os.path.join(settings.STATIC_ROOT, name)):
            os.remove(os.path.join(settings.STATIC_ROOT, name))
        return name