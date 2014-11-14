from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import ListView, DetailView, View
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse_lazy

from bees.models import DUser, History
from bees.forms import DUserForm

def index(request):
    return render(request, 'index.html')

class UserCheckMixin(object):
    user_check_failure_path = reverse_lazy('login')

    def check_user(self, user):
        return user.is_authenticated()

    def user_check_failed(self, request, *args, **kwargs):
        return redirect(self.user_check_failure_path)

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user(request.user):
            return self.user_check_failed(request, *args, **kwargs)
        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)

class HiveView(UserCheckMixin, DetailView):

    template_name = 'history.html'
    model = DUser

    def dispatch(self, request, *args, **kwargs):
        if not kwargs:
            user = self.request.user
            if user.is_authenticated:
                d = DUser.objects.filter(user=user.id)
                if d:
                    return redirect(d[0])
                return redirect('beekeeper-settings')
            return HttpResponseBadRequest
        return super(HiveView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        self.duser = get_object_or_404(DUser, d_id=self.kwargs['d_id'])
        return self.duser

    def get_queryset(self):
        return  History.objects.filter(duser=self.duser)

    def get_context_data(self, **kwargs):
        context = super(HiveView, self).get_context_data(**kwargs)
        context['duser'] = self.duser
        context['hists'] = self.get_queryset()
        context['bees'] = self.duser.bees_dict
        context['updated'] = self.duser.updated
        return context

class SettingsView(UserCheckMixin, View):
    template_name = 'settings.html'
    form_class = DUserForm

    def get_object(self):
        duser = DUser.objects.filter(user=self.request.user.id)
        self.duser = None
        if duser:
            self.duser = duser[0]
        return self.duser

    def get_context_data(self, **kwargs):
        context = dict(**kwargs)
        if not self.duser:
            context['new_user'] = True
        else:
            context['confirmed'] = self.duser.confirmed
        return context

    def form_invalid(self, form):
        d_user = self.get_object()
        context = self.get_context_data(form=form)
        return self.render_to_response(context=context)

    def render_to_response(self, context):
        return TemplateResponse(
                request=self.request,
                template=self.template_name,
                context=context)

    def form_valid(self, form):
        d_user = self.get_object()
        new_d_user = form.save(commit=False)
        new_d_user.user = self.request.user
        if d_user:
            d_user.d_id = new_d_user.d_id
        else:
            d_user = new_d_user
        d_user.save()
        return redirect('beekeeper-settings')

    def get(self, request, *args, **kwargs):
        d_user = self.get_object()
        if d_user:
            form = self.form_class(initial={'d_id':d_user.d_id})
        else:
            form = self.form_class()
        context = self.get_context_data(form=form)
        return self.render_to_response(context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
