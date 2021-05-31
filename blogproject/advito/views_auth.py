from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView, UpdateView
from django.http.response import Http404
from django.contrib.auth.models import User
from .forms_auth import LoginForm, SignUpForm, UpdateProfileForm
from .models import Profile, Post, CategoryPost


class Login(LoginView):
    template_name = 'my_auth/login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            # cleaned_data - словарь
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse('advito:index'), request)
        
        return render(request, self.template_name, context={'form':form})

@login_required
def logout_views(request):
    logout(request)
    return redirect(reverse("advito:index"))


class SignUpView(View):
    template_name = 'my_auth/signup.html'
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form': self.form_class()})

    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        registered = False
        context = {}
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            registered = True
        else:
            context.update({'form': form})

        context.update({'registered': registered})
        return render(request, self.template_name, context=context)


class ProfileView(DetailView):
    model = Profile
    template_name = 'my_auth/profile.html'
    
    # Метод get_object Получит объект профиля и передаст его на страницу
    def get_object(self):
        return get_object_or_404(self.model, user__id=self.kwargs['user_id'])


class UpdateProfileView(UpdateView):
    model = Profile #модель для обновления
    form_class = UpdateProfileForm
    template_name = 'my_auth/profile_update.html'
    slug_field = "user_id"
    slug_url_kwarg = "user_id"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise Http404("It's not your profile")
        return super(UpdateProfileView, self).dispatch(request, *args, **kwargs)

    # Перенаправление пользователя после выполенния всех действий
    def get_success_url(self):
        user_id = self.kwargs['user_id']
        return reverse('advito:profile', args=(user_id, ))


def profile_posts(request, user_id):
    categories= CategoryPost.objects.all()
    template_name = 'advito/index.html'
    profile_posts = Post.objects.filter(author_id=user_id, date_pub__year=2021).order_by('-date_pub')[:10]
    
    context = {'categories':categories, 'posts': profile_posts}
    return render(request, template_name, context)


def profile_message(request, user_id):
    model = Profile
    categories= CategoryPost.objects.all()
    template_name = 'my_auth/profile_message.html'
    
    context = {'categories':categories, }
    return render(request, template_name, context)

def profile_comment(request, user_id):
    categories= CategoryPost.objects.all()
    template_name = 'my_auth/profile_comment.html'
    
    context = {'categories':categories, }
    return render(request, template_name, context)
