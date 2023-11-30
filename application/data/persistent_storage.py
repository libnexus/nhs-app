from json import loads, dumps
from os.path import isfile, abspath


class PersistentStorage(dict):
    def __init__(self, file_path: str):
        super().__init__()
        self._file_path = abspath(file_path + ".hidden")
        if isfile(self._file_path):
            with open(self._file_path, "r") as file:
                self.update(loads(file.read()))

    def save(self):
        with open(self._file_path, "w+") as file:
            file.write(dumps(self))
        # SetFileAttributes(self._file_path, FILE_ATTRIBUTE_HIDDEN)


APP_CONFIG = PersistentStorage("nhs-app.conf")
