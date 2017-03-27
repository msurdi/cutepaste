import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from cutepaste.tests.marks import slow

pytestmark = pytest.mark.usefixtures("data_files")


@slow
def test_index(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))
    directories = webdriver.find_elements_by_css_selector(".dir-item")
    files = webdriver.find_elements_by_css_selector(".file-item")
    assert len(directories) == 1
    assert len(files) == 2


@slow
def test_navigate_to_directory(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))

    dir1_links = webdriver.find_elements_by_link_text("dir1/")
    assert len(dir1_links) == 1

    dir1_link = dir1_links[0]

    dir1_link.click()

    dir1_file1_links = webdriver.find_elements_by_link_text("dir1_file1.txt")

    assert len(dir1_file1_links) == 1


@slow
def test_remove_file(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1

    file1_checkboxes = webdriver.find_elements_by_css_selector("input[data-entry='file1.txt']")
    assert len(file1_checkboxes) == 1

    file1_checkbox = file1_checkboxes[0]
    file1_checkbox.click()

    trash_button = webdriver.find_element_by_id("trash-button")

    trash_button.click()

    WebDriverWait(webdriver, 1).until(
        EC.invisibility_of_element_located((By.LINK_TEXT, "file1.txt")))

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 0


@slow
def test_copy_paste_file(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1

    file1_checkboxes = webdriver.find_elements_by_css_selector("input[data-entry='file1.txt']")
    assert len(file1_checkboxes) == 1

    file1_checkbox = file1_checkboxes[0]
    file1_checkbox.click()

    copy_button = webdriver.find_element_by_id("copy-button")

    copy_button.click()

    dir1_links = webdriver.find_elements_by_link_text("dir1/")
    assert len(dir1_links) == 1

    dir1_link = dir1_links[0]

    dir1_link.click()

    WebDriverWait(webdriver, 1).until(
        EC.invisibility_of_element_located((By.LINK_TEXT, "file1.txt")))

    paste_button = webdriver.find_element_by_id("paste-button")

    paste_button.click()

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1

    dir_up_links = webdriver.find_elements_by_link_text("../")
    assert len(dir_up_links) == 1

    dir_up_link = dir_up_links[0]

    dir_up_link.click()

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1

