from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'image', 'uploaded_at']
    search_fields = ['name']
    list_filter = ['uploaded_at']