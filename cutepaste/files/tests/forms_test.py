import pytest
from django.http import QueryDict

from ..forms import FilesEditForm
from ..models import File


@pytest.fixture(name="valid_form")
def fixture_valid_form():
    file1 = File("/data/file1", "/file1")
    file2 = File("/data/file2", "/file2")
    post_data = QueryDict(mutable=True)
    post_data["/file1"] = "/file1_renamed"
    return FilesEditForm(post_data, files=[file1, file2])


def test_valid_form(valid_form):
    field1 = valid_form.fields["/file1"]
    assert len(valid_form.fields) == 2
    assert field1.required
    assert field1.label == "file1"
    assert len(field1.validators) == 1
