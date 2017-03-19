from typing import List

from django import forms
from django.core.validators import RegexValidator

from cutepaste.files.models import FSEntry


class FilesEditForm(forms.Form):
    def __init__(self, *args, files: List[FSEntry], **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for file in files:
            self.fields[file.relative_path] = forms.CharField(
                label=file.name,
                initial=file.name,
                required=True,
                validators=[
                    RegexValidator(
                        inverse_match=True,
                        regex=r"/",
                        message="File name cannot contain '/'",
                        code="invalid_name"
                    ),
                ]
            )
