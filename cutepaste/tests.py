import subprocess
import sys

from flake8.api import legacy as flake8


def test_flake8_compliance():
    pep8style = flake8.get_style_guide(config_file=".flake8")
    result = pep8style.check_files(["cutepaste"])
    assert result.total_errors == 0


def test_mypy_compliance():
    result = subprocess.call("/usr/local/bin/mypy --silent-imports cutepaste",
                             shell=True,
                             stdout=sys.stdout,
                             stderr=sys.stderr)
    assert result == 0
