from django.conf.urls import patterns, url

from bees.views import index, RegistrationView

urlpatterns = patterns('',
    url(r'registration/', RegistrationView.as_view(), name='registration'),
    url(r'.*', index, name='index'),
)
