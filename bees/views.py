from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import ListView, DetailView, View
from django.template.response import TemplateResponse

from bees.models import DUser, History
from bees.forms import DUserForm

def index(request):
    return render(request, 'index.html')

class HiveView(DetailView):

    template_name = 'history.html'
    model = DUser

    def dispatch(self, request, *args, **kwargs):
        if not kwargs:
            user = self.request.user
            if user.is_authenticated:
                d = DUser.objects.get(user=user.id)
                if d:
                    return redirect(d)
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
        return context

class SettingsView(View):
    template_name = 'settings.html'
    form_class = DUserForm

    def get_object(self):
        duser = DUser.objects.filter(user=self.request.user.id)
        self.duser = None
        if duser:
            self.duser = duser[0]
        return self.duser

    def get_context_data(self, **kwargs):
        return dict(**kwargs)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context=context)

    def render_to_response(self, context):
        return TemplateResponse(
                request=self.request,
                template=self.template_name,
                context=context)

    def form_valid(self, form):
        d_user = form.save(commit=False)
        d_user.user = self.request.user
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
