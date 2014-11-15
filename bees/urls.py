from django.conf.urls import patterns, url

from bees.views import index, HiveView, SettingsView, authorize

urlpatterns = patterns('',
    url(r'^beekeeper/$', SettingsView.as_view(), name='beekeeper-settings'),
    url(r'^hive/(?P<d_id>\d+)/$', HiveView.as_view(), name='hive-detail'),
    url(r'^hive/$', HiveView.as_view(), name='hive-detail'),
    url(r'^authorize/$', authorize, name='authorize'),
    url(r'^$', index, name='index'),
)
