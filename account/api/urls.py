from django.conf.urls import url
from account.api.views import NoteAPIView, LoginAPIView, CreateUserAPIView
from rest_framework_jwt.views import RefreshJSONWebToken

app_name = 'account-api'
urlpatterns = [
    # TODO = Refresh the JSON WEB TOKEN
    url(r'^token-refresh$', RefreshJSONWebToken.as_view()),
    url(r'^login$', LoginAPIView.as_view()),
    url(r'^create$', CreateUserAPIView.as_view()),
]
