import uuid
from django.db import models
from .storage import OverwriteStorage


STORAGE = OverwriteStorage(location="_public/static")

TYPE_IMAGE_CHOICES = (
    ("JPEG", "jpeg"),
    ("PNG", "png")
)


class DeepSlide(models.Model):
    slug = models.UUIDField('Slug', primary_key=False, default=uuid.uuid4, editable=False)
    type_image = models.CharField('Tipo da imagem', choices=TYPE_IMAGE_CHOICES, max_length=255, blank=True, null=True)
    image = models.FileField('Imagem', storage=STORAGE, blank=True, null=True)
    file_dzi = models.CharField('Arquivo DZI', max_length=1000, blank=True, null=True)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url