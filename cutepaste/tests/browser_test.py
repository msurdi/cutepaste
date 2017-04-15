import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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

    dir1_links = webdriver.find_elements_by_link_text("dir1")
    assert len(dir1_links) == 1

    dir1_link = dir1_links[0]

    dir1_link.click()

    dir1_file1_links = webdriver.find_elements_by_link_text("dir1_file1.txt")

    assert len(dir1_file1_links) == 1


@slow
def test_breadcrumbs(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))

    home_breacrumb = webdriver.find_elements_by_css_selector("a[href='/ls/']")

    assert len(home_breacrumb) == 1


@slow
def test_breadcrumbs_in_subdirs(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=["dir1/subdir1"]))

    WebDriverWait(webdriver, 6).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#breadcrumbs li")))

    breadcrumbs_list = webdriver.find_elements_by_css_selector("#breadcrumbs li")

    assert len(breadcrumbs_list) == 3

    breadcrumb_parent = webdriver.find_elements_by_css_selector("a[href='/ls/dir1']")

    assert len(breadcrumb_parent) == 1


@slow
def test_remove_file(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1

    file1_checkboxes = webdriver.find_elements_by_css_selector("input[value='file1.txt']")
    assert len(file1_checkboxes) == 1

    file1_checkbox = file1_checkboxes[0]
    file1_checkbox.click()

    trash_button = webdriver.find_element_by_id("trash-button")

    trash_button.click()

    confirm_trash_button = webdriver.find_element_by_id("confirm-trash-button")
    confirm_trash_button.click()

    WebDriverWait(webdriver, 1).until(
        EC.invisibility_of_element_located((By.LINK_TEXT, "file1.txt")))

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 0


@slow
def test_copy_paste_file(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1

    file1_checkboxes = webdriver.find_elements_by_css_selector("input[value='file1.txt']")
    assert len(file1_checkboxes) == 1

    file1_checkbox = file1_checkboxes[0]
    file1_checkbox.click()

    copy_button = webdriver.find_element_by_id("copy-button")

    copy_button.click()

    dir1_links = webdriver.find_elements_by_link_text("dir1")
    assert len(dir1_links) == 1

    dir1_link = dir1_links[0]

    dir1_link.click()

    WebDriverWait(webdriver, 1).until(
        EC.invisibility_of_element_located((By.LINK_TEXT, "file1.txt")))

    paste_button = webdriver.find_element_by_id("paste-button")

    paste_button.click()

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1

    dir_up_links = webdriver.find_elements_by_css_selector("a[href='/ls/']")
    assert len(dir_up_links) == 1

    dir_up_link = dir_up_links[0]

    dir_up_link.click()

    WebDriverWait(webdriver, 1).until(
        EC.invisibility_of_element_located((By.LINK_TEXT, "dir1_file1.txt")))

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1


@slow
def test_cut_paste_file(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1

    file1_checkboxes = webdriver.find_elements_by_css_selector("input[value='file1.txt']")
    assert len(file1_checkboxes) == 1

    file1_checkbox = file1_checkboxes[0]
    file1_checkbox.click()

    cut_button = webdriver.find_element_by_id("cut-button")

    cut_button.click()

    dir1_links = webdriver.find_elements_by_link_text("dir1")
    assert len(dir1_links) == 1

    dir1_link = dir1_links[0]

    dir1_link.click()

    WebDriverWait(webdriver, 1).until(
        EC.invisibility_of_element_located((By.LINK_TEXT, "file1.txt")))

    paste_button = webdriver.find_element_by_id("paste-button")

    paste_button.click()

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1

    dir_up_links = webdriver.find_elements_by_css_selector("a[href='/ls/']")
    assert len(dir_up_links) == 1

    dir_up_link = dir_up_links[0]

    dir_up_link.click()

    WebDriverWait(webdriver, 1).until(
        EC.invisibility_of_element_located((By.LINK_TEXT, "dir1_file1.txt")))

    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 0


@slow
def test_select_all_then_none(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))

    select_all_button = webdriver.find_element_by_id("select-all-button")

    select_all_button.click()

    checkboxes = webdriver.find_elements_by_css_selector("input[type=checkbox]")
    assert len(checkboxes) == 3
    assert all([checkbox.is_selected() for checkbox in checkboxes])

    select_none_button = webdriver.find_element_by_id("select-none-button")

    select_none_button.click()

    checkboxes = webdriver.find_elements_by_css_selector("input[type=checkbox]")
    assert len(checkboxes) == 3
    assert all([not checkbox.is_selected() for checkbox in checkboxes])


@slow
def test_buttons_visibility_no_selection_no_clipboard(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))
    assert webdriver.find_elements_by_css_selector("#select-all-button")
    assert webdriver.find_elements_by_css_selector("#edit-button")
    assert not webdriver.find_elements_by_css_selector("#select-none-button")
    assert not webdriver.find_elements_by_css_selector("#copy-button")
    assert not webdriver.find_elements_by_css_selector("#cut-button")
    assert not webdriver.find_elements_by_css_selector("#trash-button")
    assert not webdriver.find_elements_by_css_selector("#paste-button")


@slow
def test_buttons_visibility_no_selection_with_clipboard(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))

    # Select a file and copy it to the clipboard
    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1

    file1_checkboxes = webdriver.find_elements_by_css_selector("input[value='file1.txt']")
    assert len(file1_checkboxes) == 1

    file1_checkbox = file1_checkboxes[0]
    file1_checkbox.click()

    copy_button = webdriver.find_element_by_id("copy-button")

    copy_button.click()

    WebDriverWait(webdriver, 1).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#paste-button")))

    file1_checkbox.click()

    assert webdriver.find_elements_by_css_selector("#select-all-button")
    assert webdriver.find_elements_by_css_selector("#edit-button")
    assert not webdriver.find_elements_by_css_selector("#select-none-button")
    assert not webdriver.find_elements_by_css_selector("#copy-button")
    assert not webdriver.find_elements_by_css_selector("#cut-button")
    assert not webdriver.find_elements_by_css_selector("#trash-button")
    assert webdriver.find_elements_by_css_selector("#paste-button")


@slow
def test_buttons_visibility_with_selection_no_clipboard(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))

    # Select a file and copy it to the clipboard
    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1

    file1_checkboxes = webdriver.find_elements_by_css_selector("input[value='file1.txt']")
    assert len(file1_checkboxes) == 1

    file1_checkbox = file1_checkboxes[0]
    file1_checkbox.click()

    assert webdriver.find_elements_by_css_selector("#select-all-button")
    assert webdriver.find_elements_by_css_selector("#edit-button")
    assert webdriver.find_elements_by_css_selector("#select-none-button")
    assert webdriver.find_elements_by_css_selector("#copy-button")
    assert webdriver.find_elements_by_css_selector("#cut-button")
    assert webdriver.find_elements_by_css_selector("#trash-button")
    assert not webdriver.find_elements_by_css_selector("#paste-button")


@slow
def test_buttons_visibility_with_selection_with_clipboard(live_server, webdriver):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))

    # Select a file and copy it to the clipboard
    file1_links = webdriver.find_elements_by_link_text("file1.txt")
    assert len(file1_links) == 1

    file1_checkboxes = webdriver.find_elements_by_css_selector("input[value='file1.txt']")
    assert len(file1_checkboxes) == 1

    file1_checkbox = file1_checkboxes[0]
    file1_checkbox.click()

    copy_button = webdriver.find_element_by_id("copy-button")

    copy_button.click()

    WebDriverWait(webdriver, 1).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#select-none-button")))

    assert webdriver.find_elements_by_css_selector("#select-all-button")
    assert webdriver.find_elements_by_css_selector("#edit-button")
    assert webdriver.find_elements_by_css_selector("#select-none-button")
    assert webdriver.find_elements_by_css_selector("#copy-button")
    assert webdriver.find_elements_by_css_selector("#cut-button")
    assert webdriver.find_elements_by_css_selector("#trash-button")
    assert webdriver.find_elements_by_css_selector("#paste-button")
