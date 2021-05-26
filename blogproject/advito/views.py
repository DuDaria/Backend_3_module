from django.contrib.auth import login, authenticate
from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.views.generic import (View, ListView, 
    CreateView, DeleteView, UpdateView, DetailView
)
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import (Post, Comment, Profile, 
    CategoryPost, FavoritePost, Review, Message
)
from .forms import (PostForm, ProfileForm, PersonalForm, 
    CommentForm, MessageForm
)


class IndexView(ListView):
    categories = CategoryPost.objects.all()
    model = Post 
    template_name = 'advito/index.html'
    context_object_name ='posts'
    extra_context = {'categories':categories, }

    def get_queryset(self):
        return self.model.objects.filter(date_pub__year=2021).order_by('-date_pub')[:15]


def support(request):
    template_name = 'advito/support.html'
    return render(request, template_name)


class PostDetailView(DetailView):
    categories = CategoryPost.objects.all()
    extra_context = {'categories':categories, }
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'advito/post_detail.html'
    comment_form_class = CommentForm
    context={}
    
    def get(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        profile = Profile.objects.get(user=self.object.author)
        context = self.get_context_data(object=self.object)
        context['profile'] = profile
        context['comments'] = Comment.objects.filter(in_post__id=post_id).order_by('-date_publish')

        if request.user.is_authenticated:
            context['comment_form'] = self.comment_form_class()

        return self.render_to_response(context)
        
    list = []
    @method_decorator(login_required(login_url='/advito/login/'))
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        form = self.comment_form_class(request.POST)

        if form.is_valid():
            print("Форма валидна!")
            comment = form.save(commit=False)
            comment.author = request.user
            comment.in_post = post
            comment.save()
            return redirect(request.META.get('HTTP_REFERER'), request)
        
        elif 'button_add_post' in request.POST:
            if request.user:
                self.list.append(post)
                print(self.list)
                print("Hello")
                return redirect(reverse('advito:favorite_post'))
        else:
            print("Форма не валидна!")
            return render(request, self.template_name, context={
                'comment_form': self.comment_form_class,
                'post': post,
                'comments': Comment.objects.filter(in_post__id=post_id).order_by('-date_publish')
            })


class PostEditView(UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'advito/post_edit.html'
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise PermissionDenied ("Вы не автор этого поста!!!")
        
        return super(PostEditView, self).dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        post_id = self.kwargs[self.pk_url_kwarg]
        print(post_id)
        return reverse('advito:post_detail', args=(post_id, ))


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = 'advito/post_create.html'
    
    @method_decorator(login_required(login_url='/advito/login/'))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            print("Форма валидна!")
            post_form = form.save(commit=False) 
            post_form.author = request.user 
            post_form.save()
            post_new_id = post_form.id
            post_new = Post.objects.get(id=post_new_id)
            context['post_was_created'] = True
            context['post_new'] = post_new
        else:
            print("Форма не валидна")
            context['post_with_errors'] = True
            context['form'] = form
        
        return render(request, self.template_name, context)


class PostDeleteView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'advito/post_delete.html'

    # переопределим метод (получение ссылки advito:post_delete_success)
    def get_success_url(self):
        post_id = self.kwargs[self.pk_url_kwarg]
        print(post_id)
        return reverse('advito:post_delete_success', args=(post_id, ))


class FavoritePostView(ListView):
    model = Post
    post_form_class = PostForm
    categories = CategoryPost.objects.all()
    template_name = 'advito/favorite_post.html'
    context_object_name ='add_posts'
    extra_context = {'categories':categories, }
    context = {}

    # метод возвращает строчку
    def get_queryset(self):
        return self.model.objects.filter(date_pub__year=2021).order_by('-date_pub')[:15]
    

def category_post(request, category_id):
    name = request.user.username
    category_queryset = Post.objects.filter(category=category_id, date_pub__year=2021).order_by('-date_pub')[:10]
    categories= CategoryPost.objects.all()
    template_name = 'advito/index.html'
    context = {'categories':categories, 'posts': category_queryset, 'name':name}
    
    return render(request, template_name, context)


def profile(request):
    name = request.user.username
    template_name = 'advito/profile.html'
    user = request.user.id

    context = {'profile': ProfileForm(), 'name': name, 'user':user}
    return render(request, template_name, context)


def personal_info(request, user_id):
    name = request.user.username 
    first_name = request.user.first_name
    email = request.user.email
    template_name = 'advito/personal_info.html'

    context = {
        'personal_info': PersonalForm(), 
        'name': name, 
        'email': email, 
        'first_name': first_name,
    }
    return render(request, template_name, context)

