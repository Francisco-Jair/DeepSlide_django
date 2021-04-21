from django.shortcuts import render
from io import BytesIO
from openslide import open_slide
from openslide.deepzoom import DeepZoomGenerator
import re
from unicodedata import normalize
from .models import DeepSlideDynamica
from django.http import HttpResponse, Http404
from django.conf import settings
from os import path
from threading import Lock 


class Openslides:
    _slides = {}
    _deepzooms = {}
    _dict_lock = Lock()

    def __init__(self):
        pass
    
    @classmethod
    def insertslide(cls, key, sl):
        # opts = {'tile_size': settings.DEEPZOOM_TILE_SIZE, 'overlap': settings.DEEPZOOM_OVERLAP}
        opts = {'tile_size': 254, 'overlap': 1}
        with cls._dict_lock:
            cls._slides[key] = sl
            cls._deepzooms[key] = DeepZoomGenerator(sl, **opts)
            
    @classmethod
    def getslide(cls, key):
        with cls._dict_lock:
            return cls._slides[key]

    @classmethod
    def getdeepzoom(cls, key):
        with cls._dict_lock:
            return cls._deepzooms[key]

"""
class PILBytesIO(BytesIO):
    def fileno(self):
        '''Classic PIL doesn't understand io.UnsupportedOperation.'''
        raise AttributeError('Not supported')


def slugify(text):
    text = normalize('NFKD', text.lower()).encode('ascii', 'ignore').decode()
    return re.sub('[^a-z0-9]+', '-', text)
"""

def index(request):

    try:
        objeto = DeepSlideDynamica.objects.get(id=1)
    except DoesNotExist:
        raise Http404
    # osr = open_slide(objeto.image.path)
    # slide = DeepZoomGenerator(osr)

    context = {
        "slide_filename" : "Imagem Slide",
        # "slide_url" : slide_url,
        "slide_obj" : objeto,
    }

    return render(request, 'core/index.html', context)


def load_slide(slide_id, slidefile):
    sl = open_slide(slidefile)
    Openslides.insertslide(slide_id, sl)


def get_deepzoom(slide_id):

    if slide_id not in Openslides._slides:
        s = DeepSlideDynamica.objects.get(id=1)
        load_slide(s.pk, path.join(settings.HISTOSLIDE_SLIDEROOT, s.image.path))
    
    return Openslides.getdeepzoom(slide_id)


def dzi(request, slug):
    
    slideformat = 'jpeg'

    try:
        slug = int(slug)
        resp = HttpResponse(get_deepzoom(slug).get_dzi(slideformat), content_type='application/xml')
        return resp
    except KeyError:
        raise Http404

def dztile(request, slug, level, col, row, slideformat):
    slideformat = slideformat.lower()
    slug = int(slug)
    level = int(level)
    col = int(col)
    row = int(row)

    if slideformat != 'jpeg' and slideformat != 'png':
        # não suportado pelo DeepZoom
        raise Http404

    try:
        tile = get_deepzoom(slug).get_tile(level, (col, row))
    except KeyError:
        #Slug desconhecido
        raise Http404
    except ValueError:
        #Coordenadas Erradas
        raise Http404
    
    buf = BytesIO()
    tile.save(buf, slideformat, quality=100)
    resp = HttpResponse(buf.getvalue(), content_type='image/%s' % slideformat)
    return resp




