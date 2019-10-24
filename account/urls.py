from django.conf.urls import url
from account.views import log_in, home

app_name = 'index'
urlpatterns = [
    url(r'^login$', log_in, name='login'),
    url(r'^$', home, name='home'),
]
