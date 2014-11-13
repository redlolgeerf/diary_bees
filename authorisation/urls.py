from django.conf.urls import patterns, url

from authorisation.views import user_logout, LoginView, RegistrationView

urlpatterns = patterns('',
    url(r'registration/', RegistrationView.as_view(), name='registration'),
    url(r'login/', LoginView.as_view(), name='login'),
    url(r'logout/', user_logout, name='logout'),
    )
