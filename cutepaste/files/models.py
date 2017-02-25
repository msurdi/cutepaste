from os import path


class FSEntry:
    def __init__(self, absolute_path: str, relative_path: str) -> None:
        self._absolute_path = absolute_path
        self._relative_path = relative_path

    def is_file(self) -> bool:
        return path.isfile(self._absolute_path)

    def is_dir(self) -> bool:
        return path.isdir(self._absolute_path)

    def name(self) -> str:
        return path.basename(self._absolute_path)

    def relative_path(self) -> str:
        return self._relative_path
