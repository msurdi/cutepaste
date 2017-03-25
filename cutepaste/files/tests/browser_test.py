import pytest
from django.urls import reverse
from selenium.webdriver import Firefox
from pyvirtualdisplay import Display


@pytest.yield_fixture(scope='session')
def webdriver():
    display = Display(visible=0, size=(800, 600), use_xauth=True)
    display.start()
    driver = Firefox()
    yield driver
    driver.quit()
    display.stop()


@pytest.mark.slow
def test_on_browser(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=["/"]))
    print(webdriver.page_source)
    all_items = webdriver.find_elements_by_css_selector(".list-group-item")
    assert len(all_items) > 0
