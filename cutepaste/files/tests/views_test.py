from .. import views


class FSEntryMock:
    def __init__(self, name: str, is_file: bool = True):
        self.name = name
        self.is_file = is_file
        self.is_dir = not is_file
        self.relative_path = f"/{name}"
        self.absolute_path = f"/data/{name}"


def test_ls_directory(rf, mocker):
    ls_mock = mocker.patch("cutepaste.files.views.service.ls")
    ls_mock.return_value = [FSEntryMock("file1"), FSEntryMock("file2")]

    stat_mock = mocker.patch("cutepaste.files.views.service.stat")
    stat_mock.return_value = FSEntryMock("/", is_file=False)
    request = rf.get("/")
    request.session = {}
    response = views.ls(request, "/")
    response_body = response.content.decode("utf-8")
    assert response.status_code == 200
    assert 'href="/browse/file1"' in response_body
    assert 'href="/browse/file2"' in response_body
