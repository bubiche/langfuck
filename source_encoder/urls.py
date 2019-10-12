from django.urls import path

from .views import homepage, encode_file


urlpatterns = [
    path('', homepage, name='homepage'),
    path('encode/', encode_file)
]