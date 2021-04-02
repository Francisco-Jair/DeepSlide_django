import uuid
import os
import openslide
import threading
from django.db import models
from .storage import OverwriteStorage
from openslide import open_slide
from openslide.deepzoom import DeepZoomGenerator
from django.conf import settings   


"""
x = threading.Thread(target=thread_function, args=(1,))
    x.start()
"""


STORAGE = OverwriteStorage(location="_public/static")


TYPE_IMAGE_CHOICES = (
    ("JPEG", "jpeg"),
    ("PNG", "png")
)

def generate_image_slide(slide, path_folder, format_image="jpeg"):

    # if not os.path.exists(path_folder):
    #     os.makedirs(path_folder)

    for level in range(slide.level_count):
        
        path_folder_level = os.path.join(path_folder, str(level))
        if not os.path.exists(path_folder_level):
            os.makedirs(path_folder_level)
        
        cols, rows = slide.level_tiles[level]

        for row in range(rows):
            for col in range(cols):

                name_tile = f'{str(col)}_{str(row)}.{format_image}'
                dir_tile = os.path.join(path_folder_level, name_tile)

                tile = slide.get_tile(level, (col, row))

                if not os.path.exists(dir_tile):
                    tile.save(dir_tile, format=format_image, quality=100)



def load_dzi(path, slug, format_image="jpeg"):

    osr = open_slide(path)
    slide = DeepZoomGenerator(osr)

    # create folder
    name_folder = os.path.join(settings.SLIDE_FOLDER, str(slug))
    if not os.path.exists(name_folder):
        os.makedirs(name_folder)

    #Generate file DZI
    slide_dzi = slide.get_dzi(format_image)
    path_save_dzi = os.path.join(name_folder, f'slide_{slug}.dzi')


    with open(path_save_dzi, 'w') as fh:
        fh.write(path_save_dzi)

    # File slide
    path_save_folder = os.path.join(name_folder, f'slide_{slug}')
    if not os.path.exists(path_save_folder):
        os.makedirs(path_save_folder)

    generate_image_slide(slide, path_save_folder, format_image)
    # trh = 

    return path_save_dzi


class DeepSlide(models.Model):
    slug = models.UUIDField('Slug', primary_key=False, default=uuid.uuid4, editable=False)
    type_image = models.CharField('Tipo da imagem', choices=TYPE_IMAGE_CHOICES, max_length=255, blank=True, null=True)
    image = models.FileField('Imagem', storage=STORAGE, blank=True, null=True)
    file_dzi = models.CharField('Arquivo DZI', max_length=1000, blank=True, null=True)
    #mpp


    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        
    
    def save(self, *args, **kwargs):
        self.file_dzi = load_dzi(self.image.path, self.slug, self.type_image)
        super(DeepSlide, self).save(*args, **kwargs)
        # self.save()
        # save()


class DeepSlideDynamica(models.Model):
    slug = models.UUIDField('Slug', primary_key=False, default=uuid.uuid4, editable=False)
    type_image = models.CharField('Tipo da imagem', choices=TYPE_IMAGE_CHOICES, max_length=255, blank=True, null=True)
    image = models.FileField('Imagem', storage=STORAGE, blank=True, null=True)
    #mpp

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url