from unittest.mock import call

from django.http import HttpResponse

from .. import views


class FSEntryMock:
    def __init__(self, name: str, is_file: bool = True) -> None:
        self.name = name
        self.is_file = is_file
        self.is_dir = not is_file
        self.relative_path = f"{name}"
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
    assert 'href="/ls/file1"' in response_body
    assert 'href="/ls/file2"' in response_body


def test_ls_file(rf, mocker):
    def stat_results(path):
        if path == "/file1":
            return FSEntryMock("file1", is_file=True)

    stat_mock = mocker.patch("cutepaste.files.views.service.stat")
    stat_mock.side_effect = stat_results
    request = rf.get("/")

    response = views.ls(request, "/file1")

    assert response.status_code == 200
    assert response.has_header("X-Accel-Redirect")
    assert response["X-Accel-Redirect"] == "/data/file1"
    assert not response.content


def test_ls_unicode_file(rf, mocker):
    def stat_results(path):
        if path == "/unicod€ f|le":
            return FSEntryMock("unicod€ f|le", is_file=True)

    stat_mock = mocker.patch("cutepaste.files.views.service.stat")
    stat_mock.side_effect = stat_results
    request = rf.get("/unicod%E2%82%AC%20f%7Cle")

    response = views.ls(request, "/unicod%E2%82%AC%20f%7Cle")

    assert response.status_code == 200
    assert response.has_header("X-Accel-Redirect")
    assert response["X-Accel-Redirect"] == "/data/unicod%E2%82%AC%20f%7Cle"
    assert not response.content


def test_cut(rf):
    request = rf.post("/", {"selected": ["/file1", "/file2"]})
    request.session = {}

    response = views.cut(request)

    assert request.session[views.CLIPBOARD_SESSION_KEY] == ["/file1", "/file2"]
    assert request.session[views.OPERATION_SESSION_KEY] == views.CUT_OPERATION
    assert response.status_code == 200


def test_copy(rf):
    request = rf.post("/", {"selected": ["/file1", "/file2"]})
    request.session = {}

    response = views.copy(request)

    assert request.session[views.CLIPBOARD_SESSION_KEY] == ["/file1", "/file2"]
    assert request.session[views.OPERATION_SESSION_KEY] == views.COPY_OPERATION
    assert response.status_code == 200


def test_paste(rf, mocker):
    move_mock = mocker.patch("cutepaste.files.views.service.move")
    request = rf.post("/", {"some": "data", "directory": "target"})
    request.session = {views.CLIPBOARD_SESSION_KEY: ["/file1"], views.OPERATION_SESSION_KEY: views.CUT_OPERATION}

    response = views.paste(request)

    assert move_mock.mock_calls == [call(["/file1"], "target")]
    assert response.status_code == 200
    assert response.content == b'{"script": "Turbolinks.visit(\'/ls/target\')"}'
    assert request.session[views.CLIPBOARD_SESSION_KEY] == []
    assert not request.session[views.OPERATION_SESSION_KEY]


def test_trash(rf, mocker):
    remove_mock = mocker.patch("cutepaste.files.views.service.remove")
    ls_mock = mocker.patch("cutepaste.files.views.ls")
    ls_mock.return_value = HttpResponse("ls response", status=200)
    request = rf.post("/", {"selected": ["/file1"], "directory": ""})

    response = views.trash(request)

    assert remove_mock.mock_calls == [call(["/file1"])]
    assert response.status_code == 200
    assert response.content == b'{"script": "Turbolinks.visit(\'/ls/\')"}'


def test_trash_get(rf):
    request = rf.get("/")

    response = views.trash(request)

    assert response.status_code == 405


def test_edit(rf, mocker):
    mocker.patch("cutepaste.files.views.service.ls")
    request = rf.get("/")

    response = views.edit(request, "/dir")

    assert response.status_code == 200
    response_body = response.content.decode("utf-8")
    assert "<form" in response_body


def test_rename(rf, mocker):
    ls_service_mock = mocker.patch("cutepaste.files.views.service.ls")
    ls_service_mock.return_value = [FSEntryMock("dir/file1"), FSEntryMock("dir/file2")]
    ls_mock = mocker.patch("cutepaste.files.views.ls")
    ls_mock.return_value = HttpResponse("ls response", status=200)
    rename_mock = mocker.patch("cutepaste.files.views.service.rename")
    request = rf.post("/", {"dir/file1": "file1.renamed", "dir/file2": "file2", "directory": "dir"})

    response = views.rename(request)

    assert rename_mock.mock_calls == [call("dir/file1", "dir/file1.renamed")]
    assert response.status_code == 200
    assert response.content == b'{"script": "Turbolinks.visit(\'/ls/dir\')"}'
