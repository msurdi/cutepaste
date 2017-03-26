import pytest
from django.urls import reverse


@pytest.mark.slow
def test_index(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))
    directories = webdriver.find_elements_by_css_selector(".dir-item")
    files = webdriver.find_elements_by_css_selector(".file-item")
    assert len(directories) == 2
    assert len(files) == 2
