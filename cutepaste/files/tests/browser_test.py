import pytest
from django.urls import reverse


@pytest.mark.slow
def test_on_browser(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))
    all_items = webdriver.find_elements_by_css_selector(".list-group-item")
    assert len(all_items) == 1
