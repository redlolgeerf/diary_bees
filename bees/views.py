from django.shortcuts import render
from django.views.generic.edit import FormView

from bees.forms import RegisterForm

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
