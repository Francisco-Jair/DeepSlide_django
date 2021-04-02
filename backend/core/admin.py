from django.contrib import admin
from .models import DeepSlide, DeepSlideDynamica

# Register your models here.
admin.site.register(DeepSlide)
admin.site.register(DeepSlideDynamica)
# class DeepSlideAdmin(admin.ModelAdmin):
#     pass