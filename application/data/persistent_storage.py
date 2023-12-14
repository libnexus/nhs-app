import sys
from json import loads, dumps
from os.path import abspath, join


def safe_path(file: str):
    if hasattr(sys, "_MEIPASS"):
        return abspath(join(sys._MEIPASS, file))
    else:
        return "resources/" + file


class AppConfig:
    Data = {}

    @classmethod
    def restore_to_factory(cls):
        ...

    @classmethod
    def save(cls):
        open(safe_path("app.config"), "w+").write(dumps(AppConfig.Data))

    @classmethod
    def load_from_file(cls):
        data = loads(open(safe_path("app.config"), "r").read())
        cls.Data.update(data)

    @classmethod
    def add_recent_file(cls, name: str, path: str):
        cls.Data["recent"].append({"name": name, "path": path})

    @classmethod
    def get_recent_files(cls):
        return cls.Data["recent"]

    @classmethod
    def set_colour_theme(cls, name: str):
        cls.Data["theme"] = name

    @classmethod
    def get_colour_theme(cls, name: str):
        return cls.Data["theme"] == name


AppConfig.load_from_file()