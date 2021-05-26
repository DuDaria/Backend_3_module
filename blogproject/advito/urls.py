from django.conf.urls import url
from django.urls import path
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, 
    PasswordResetConfirmView, PasswordResetCompleteView
)
from . import views
from . import views_auth

app_name="advito"

urlpatterns = [
    url(r'index/', views.IndexView.as_view(), name='index'),
    path('support/', views.support, name='support'),
    path('profile/', views.profile, name='profile'), 
    path('<int:user_id>/profile/personal_info/', views.personal_info, name='personal_info'),
    path('category/<int:category_id>/', views.category_post, name='category_post'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'), 
    path('post/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/edit/', views.PostEditView.as_view(), name='post_edit'), 
    path('post/<int:post_id>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:post_id>/delete_success/', TemplateView.as_view(
        template_name='advito/delete_success.html'
    ), name='post_delete_success'),
    path('favorite_post/', views.FavoritePostView.as_view(), name='favorite_post'),


    # views_auth
    path('login/', views_auth.Login.as_view(), name='login'),
    path('logout/', views_auth.logout_views, name='logout'),
    path('signup/', views_auth.SignUpView.as_view(), name='signup'),
    path('password_reset/', PasswordResetView.as_view(
        success_url=reverse_lazy('advito:password_reset_done'),
        template_name='my_auth/password_reset.html'
    ), name='password_reset'),
    path('password_reset/done', PasswordResetDoneView.as_view(
        template_name='my_auth/password_reset_done.html'
    ), name='password_reset_done'),

    path('password_reset/<str:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('advito:password_reset_complete'),
    ), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(), name='password_resert_complete'),
]
