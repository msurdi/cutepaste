import os

import pytest
from pyvirtualdisplay import Display
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

REPORTS_DIR = "reports"


@pytest.fixture(scope='function')
def webdriver(request):
    display = Display(visible=0, size=(800, 600), use_xauth=True)
    display.start()
    options = Options()
    options.add_argument("--no-sandbox")
    driver = Chrome(chrome_options=options)
    prev_failed_tests = request.session.testsfailed

    yield driver

    if prev_failed_tests != request.session.testsfailed:
        try:
            os.makedirs(REPORTS_DIR)
        except os.error:
            pass
        test_name = request.function.__module__ + "." + request.function.__name__
        driver.save_screenshot(f"reports/{test_name}.png")
        with open(f"reports/{test_name}.html", "w") as f:
            f.write(driver.page_source)
    driver.quit()
    display.stop()
