from django.conf.urls import url
from . import views

app_name = "files"
urlpatterns = [
    url(r'^(?P<files_path>.*)$', views.ls, name="ls"),
]
