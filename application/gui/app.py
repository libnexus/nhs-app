from __future__ import annotations

from os.path import abspath
from tkinter.messagebox import showerror
from tkinter.ttk import Notebook
from tkinter import Menu

import JSONDatabaseIntermediary as jdbi


class App(Notebook):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._jdbi = jdbi.JSONDatabaseIntermediary()
        if not self._jdbi.init_db():
            showerror("Uh Oh", "The database had trouble connecting. Try restarting the program.")
            raise SystemExit

        self._operating_dir = abspath("/")

        # Menu
        # ref: https://pythonspot.com/tk-menubar/
        self._menu = Menu(self)
        file_menu = Menu(self._menu, tearoff=0)
        file_menu.add_command(label="New", command=self._file_new)
        file_menu.add_command(label="Open", command=self._file_open)
        file_menu.add_command(label="Open recent", command=self._file_open_recent)
        file_menu.add_command(label="Save As", command=self._file_save_as)
        file_menu.add_command(label="Export", command=self._file_export)
        file_menu.add_command(label="Import", command=self._file_import)
        file_menu.add_separator()
        # Added exit option in menu, not needed but nice addition
        file_menu.add_command(label="Exit", command=self.quit)
        self._menu.add_cascade(label="File", menu=file_menu)

        form_menu = Menu(self._menu, tearoff=0)
        form_menu.add_command(label="Clear", command=self._form_clear)
        form_menu.add_command(label="Copy", command=self._form_copy)
        form_menu.add_separator()
        form_menu.add_command(label="Preview", command=self._form_preview)
        self._menu.add_cascade(label="Form", menu=form_menu)

        help_menu = Menu(self._menu, tearoff=0)
        help_menu.add_command(label="User Manual", command=self._help_user_manual)
        help_menu.add_command(label="Version Info", command=self._help_version_info)
        self._menu.add_cascade(label="Help", menu=help_menu)

        self.master.config(menu=self._menu)

        self._file_menu = file_menu
        self._form_menu = form_menu
        self._help_menu = help_menu

    def _save_dict_as_json(self, dictionary: dict, file_name: str) -> bool:
        """
        Exports a dictionary to a json file with the constraint that all objects in the dictionary
        have to be serializable (i.e. dictionary, list, string, int, boolean or None)

        :param dictionary: the dictionary to be exported to a file
        :param file_name: the file to save the json as
        """

        with open(self._operating_dir + file_name, "w+") as file:
            file.write()

    def _file_new(self):
        pass

    def _file_open(self):
        pass

    def _file_open_recent(self):
        pass

    def _file_save(self):
        pass

    def _file_save_as(self):
        pass

    def _file_export(self):
        pass

    def _file_import(self):
        pass

    def _form_clear(self):
        pass

    def _form_copy(self):
        pass

    def _form_preview(self):
        pass

    def _help_user_manual(self):
        pass

    def _help_version_info(self):
        pass
