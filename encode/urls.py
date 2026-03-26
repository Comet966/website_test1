from django.urls import path
from . import views

app_name = 'encode'

urlpatterns = [
    path('', views.example, name='example'),
    path('encode/', views.encode_images, name='encode'),
    path('decode/', views.decode_images, name='decode'),
]