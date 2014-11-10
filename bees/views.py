from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout

from bees.models import DUser, History
from bees.forms import RegisterForm, LoginForm, DUserForm

def index(request):
    return render(request, 'base.html')

class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegisterForm
    success_url = '/thanks/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        user.set_password(user.password)
        user.save()
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

class HiveView(DetailView):

    template_name = 'history.html'
    model = DUser

    def get_object(self):
        self.duser = get_object_or_404(DUser, pk=self.kwargs['pk'])
        return self.duser

    def get_queryset(self):
        return  History.objects.filter(duser=self.duser)

    def get_context_data(self, **kwargs):
        context = super(HiveView, self).get_context_data(**kwargs)
        context['duser'] = self.duser
        context['hists'] = self.get_queryset()
        return context

class SettingsView(UpdateView):
    template_name = 'settings.html'
    success_url = '/beekeeper/2/'
    model = DUser
    form_class = DUserForm

    def form_valid(self, form):
        d_user = form.save(commit=False)
        d_user.user = self.request.user
        d_user.save()
        return super(SettingsView, self).form_valid(form)
