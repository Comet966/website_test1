"""
URL configuration for Django3 project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include('upload.urls')),
    path('encode/', include('encode.urls')),
    path('',views.index,name='index'),
]

# 开发环境配置媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)