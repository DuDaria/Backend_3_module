from django.conf.urls import url
from django.urls import path
from . import views

app_name="advito"

urlpatterns = [
    url(r'index/', views.index, name='index'), 
    path('category/<int:category_id>/', views.category_post, name='category_post'),
    path('post/create/', views.post_create, name='post_create'), 
    path('post/<int:post_id>/', views.post_detail, name='post_detaile'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'), 
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:post_id>/favorite/', views.favorite_post, name='favorite_post'),
]
