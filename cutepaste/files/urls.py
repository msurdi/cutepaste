from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from . import views

app_name = "files"
urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy("files:ls", args=[""]))),
    url(r'^ls/(?P<files_path>.*)$', views.ls, name="ls"),
    url(r'^edit/(?P<files_path>.*)$', views.edit, name="edit"),
    url(r'^buttons/', views.buttons, name="buttons"),
    url(r'^clipboard/trash/$', views.trash, name="trash"),
    url(r'^clipboard/cut/$', views.cut, name="cut"),
    url(r'^clipboard/copy/$', views.copy, name="copy"),
    url(r'^clipboard/paste/$', views.paste, name="paste"),
]
