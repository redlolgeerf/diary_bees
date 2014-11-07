from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout

from bees.forms import RegisterForm, LoginForm

def index(request):
    pass

class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegisterForm
    success_url = '/thanks/'

    def form_valid(self, form):
        user = form.save()
        user.set_password(user.password)
        user.save()
        return super(RegistrationView, self).form_valid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/thanks/'

    def form_valid(self, form):
        user = form.save()
        user = authenticate(username=user.username, password=user.password)
        login(self.request, user)

        return super(LoginView, self).form_valid(form)

def user_logout(request):
    logout(request)
    return redirect('index')
