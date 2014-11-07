from django.conf.urls import patterns, url

from bees.views import index

urlpatterns = patterns('',
    url(r'.*', index, name='index'),
)
