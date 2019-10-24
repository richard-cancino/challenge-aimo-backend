from django.conf.urls import url
from account.api.views import NoteAPIView, LoginAPIView, CreateUserAPIView
from rest_framework_jwt.views import RefreshJSONWebToken

app_name = 'note-api'
urlpatterns = [
    url(r'^create-list$', NoteAPIView.as_view()),
]
