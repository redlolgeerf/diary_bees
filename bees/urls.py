from django.conf.urls import patterns, url

from bees.views import index, RegistrationView, LoginView, logout

urlpatterns = patterns('',
    url(r'registration/', RegistrationView.as_view(), name='registration'),
    url(r'login/', LoginView.as_view(), name='login'),
    url(r'logout/', logout, name='logout'),
    url(r'.*', index, name='index'),
)
