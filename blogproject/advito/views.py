from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum
from .models import Post, Comment, Profile, CategoryPost, FavoritePost, Review, Message


def index(request):
    categories= CategoryPost.objects.all()
    posts = Post.objects.filter(date_pub__year=2021).order_by('-date_pub')[:10]
    return render(request, 'advito/index.html', context={'categories':categories, 'posts': posts})


def post_detail(request, post_id):
    categories= CategoryPost.objects.all()
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'advito/post_detail.html', context={'categories':categories,'post': post})


def post_edit(request, post_id):
    return HttpResponse(f"Детальное представление для редактирования поста №{post_id}")


def post_create(request):
    return HttpResponse("Создание поста")


def post_delete(request, post_id):
    return HttpResponse(f"Удаление поста №{post_id}")


def favorite_post(request, post_id):
    return HttpResponse(f"Избранный пост №{post_id}")


def category_post(request, category_id):
    category_queryset = Post.objects.filter(category=category_id)
    categories= CategoryPost.objects.all()
    return render(request, 'advito/index.html', context={'categories':categories, 'posts': category_queryset})
