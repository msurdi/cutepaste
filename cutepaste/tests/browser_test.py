from django.urls import reverse

from cutepaste.tests.marks import slow


@slow
def test_index(live_server, webdriver, data_files):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))
    directories = webdriver.find_elements_by_css_selector(".dir-item")
    files = webdriver.find_elements_by_css_selector(".file-item")
    assert len(directories) == 1
    assert len(files) == 2


@slow
def test_navigate_to_directory(live_server, webdriver, data_files):
    webdriver.get(live_server.url + reverse("files:ls", args=[""]))

    dir1_links = webdriver.find_elements_by_link_text("dir1/")
    assert len(dir1_links) == 1

    dir1_link = dir1_links[0]

    dir1_link.click()

    dir1_file1_links = webdriver.find_elements_by_link_text("dir1_file1.txt")

    assert len(dir1_file1_links) == 1
