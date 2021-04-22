from django.conf.urls import url
from django.urls import path
from .views import index1
from .views import index2

urlpatterns = [
    url(r'^$', index1, name='index-1'),
    path('index2/', index2, name='index-2'),
]