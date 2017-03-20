from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from . import views

app_name = "files"
urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy("files:ls", args=[""]))),
    url(r'^browse(?P<files_path>.*)$', views.ls, name="ls"),
    url(r'^trash(?P<files_path>.*)$', views.trash, name="trash"),
    url(r'^edit(?P<files_path>.*)$', views.edit, name="edit"),
    url(r'^clipboard/cut$', lambda r: views.clipboard(r, "cut"), name="cut"),
    url(r'^clipboard/copy$', lambda r: views.clipboard(r, "copy"), name="copy"),
    url(r'^clipboard/paste/(?P<files_path>.*)$', views.paste, name="paste"),
]
