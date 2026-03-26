from django.urls import path
from . import views

app_name = 'upload'

urlpatterns = [
    path('', views.upload_image, name='upload'),
    path('list/', views.image_list, name='list'),
    path('api/', views.api_upload, name='api'),
    path('show/', views.show_images, name='show'),
]