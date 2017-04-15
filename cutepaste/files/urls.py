from django.conf import settings
from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from . import views

app_name = "files"
urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy("files:ls", args=[""]))),
    url(r'^ls/(?P<directory>.*)$', views.ls, name="ls"),
    url(r'^edit/(?P<directory>.*)$', views.edit, name="edit"),
    url(r'^ajax/rename/$', views.rename, name="rename"),
    url(r'^ajax/trash/$', views.trash, name="trash"),
    url(fr'^ajax/select/{settings.CP_VERSION}/$', views.select, name="select"),
    url(r'^ajax/cut/$', views.cut, name="cut"),
    url(r'^ajax/copy/$', views.copy, name="copy"),
    url(r'^ajax/paste/$', views.paste, name="paste"),
    url(r'^ajax/confirm-trash/$', views.confirm_trash, name="confirm-trash"),
]
