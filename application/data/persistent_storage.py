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
    def save(cls):
        open(safe_path("app.config"), "w+").write(dumps(AppConfig.Data))

    @classmethod
    def load_from_file(cls):
        data = loads(open(safe_path("app.config"), "r").read())
        cls.Data.update(data)

    @classmethod
    def add_recent_file(cls, path: str):
        if path not in cls.Data["recent"]:
            cls.Data["recent"].append(path)
            if len(cls.Data["recent"]) > 10:
                cls.Data.pop(0)
            cls.save()

    @classmethod
    def get_recent_files(cls):
        return cls.Data["recent"]

    @classmethod
    def set_colour_theme(cls, name: str):
        cls.Data["theme"] = name
        cls.save()

    @classmethod
    def get_colour_theme(cls, name: str):
        return cls.Data["theme"] == name

    @classmethod
    def get_possible_themes(cls):
        return cls.Data["possible-themes"]


AppConfig.load_from_file()
