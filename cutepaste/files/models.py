from os import path


class FSEntry:
    def __init__(self, absolute_path: str, relative_path: str) -> None:
        self.absolute_path = absolute_path
        self.relative_path = relative_path

    @property
    def is_file(self) -> bool:
        return path.isfile(self.absolute_path)

    @property
    def is_dir(self) -> bool:
        return path.isdir(self.absolute_path)

    @property
    def name(self) -> str:
        return path.basename(self.absolute_path)
