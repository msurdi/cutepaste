from django.conf.urls import include, url
from django.urls import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy("files:index"))),
    url(r'^browse/', include("cutepaste.files.urls", namespace="files")),
]
