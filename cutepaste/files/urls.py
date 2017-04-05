from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from . import views

app_name = "files"
urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy("files:ls", args=[""]))),
    url(r'^ls/(?P<current_path>.*)$', views.ls, name="ls"),
    url(r'^edit/(?P<current_path>.*)$', views.edit, name="edit"),
    url(r'^ajax/rename/$', views.rename, name="rename"),
    url(r'^ajax/trash/$', views.trash, name="trash"),
    url(r'^ajax/select/$', views.select, name="select"),
    url(r'^ajax/cut/$', views.cut, name="cut"),
    url(r'^ajax/copy/$', views.copy, name="copy"),
    url(r'^ajax/paste/$', views.paste, name="paste"),
]
