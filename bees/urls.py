from django.conf.urls import patterns, url

from bees.views import logout, LoginView, RegistrationView
from bees.views import index, HiveView, SettingsView

urlpatterns = patterns('',
    url(r'registration/', RegistrationView.as_view(), name='registration'),
    url(r'login/', LoginView.as_view(), name='login'),
    url(r'logout/', logout, name='logout'),
    url(r'^beekeeper/(?P<pk>\d+)/$', SettingsView.as_view(), name='beekeeper-settings'),
    url(r'^hive/(?P<pk>\d+)/$', HiveView.as_view(), name='hive-detail'),
    url(r'^$', index, name='index'),
)
