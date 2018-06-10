from django.contrib import admin
from .models import Photo, Album


# Register your models here.

# Models' admin panel classes
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'upload_date']
    list_filter = ['upload_date']
    list_display_links = ['id', 'name']


class AlbumAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
    list_display_links = ['id']


# My models' admin panel's registers
admin.site.register(Photo, PhotoAdmin)
# admin.site.register(Face)
# admin.site.register(Identity)
admin.site.register(Album, AlbumAdmin)
