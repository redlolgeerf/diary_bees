from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from authorisation.forms import LoginForm, RegisterForm

class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegisterForm
    success_url = '/thanks/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        password = user.password
        user.set_password(user.password)
        user.save()
        user = authenticate(username=user.username, password=password)
        login(self.request, user)
        return super(RegistrationView, self).form_valid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/thanks/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user = authenticate(username=user.email, password=user.password)
        if user is not None:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            form.add_error('__all__', "User not found.")
            return super(LoginView, self).form_invalid(form)

def user_logout(request):
    logout(request)
    return redirect('index')
