from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views.generic import View
from .forms_auth import LoginForm, SignUpForm, UpdateProfileForm


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

