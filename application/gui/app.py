from __future__ import annotations

import json
import copy
from collections import deque
from os.path import abspath
from tkinter import Menu, Tk, messagebox
from tkinter import filedialog
from tkinter.messagebox import showerror
from tkinter.ttk import Notebook

import JSONDatabaseIntermediary as jdbi
import application.gui.form as form


class App(Notebook):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._jdbi = jdbi.JSONDatabaseIntermediary()
        if not self._jdbi.init_db():
            showerror("Uh Oh", "The database had trouble connecting. Try restarting the program.")
            raise SystemExit

        self._operating_dir = abspath("/")
        self._file_path = None
        # Add a list to store recent files
        self.recent_files = deque(maxlen=5)

        # Menu
        # ref: https://pythonspot.com/tk-menubar/
        self._menu = Menu(self)
        file_menu = Menu(self._menu, tearoff=0)
        file_menu.add_command(label="New", command=self._file_new)
        file_menu.add_command(label="Open", command=self._file_open)
        # file_menu.add_command(label="Open recent", command=self._file_open_recent)
        # ref: https://coderslegacy.com/python/create-submenu-in-tkinter/
        recent_menu = Menu(self._menu, tearoff=0)
        file_menu.add_cascade(label="Open recent", menu=recent_menu)

        file_menu.add_command(label="Save", command=self._file_save)
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

        self.winfo_toplevel().config(menu=self._menu)

        self._recent_menu = recent_menu
        self._file_menu = file_menu
        self._form_menu = form_menu
        self._help_menu = help_menu

        self._form_data = self._current_form_data()

    def _save_dict_as_json(self, dictionary: dict, file_name: str) -> bool:
        """
        Exports a dictionary to a json file with the constraint that all objects in the dictionary
        have to be serializable (i.e. dictionary, list, string, int, boolean or None)

        :param dictionary: the dictionary to be exported to a file
        :param file_name: the file to save the json as
        """

        with open(self._operating_dir + file_name, "w+") as file:
            file.write(...)

    def _file_new(self):
        current_form_data = self._current_form_data()

        if current_form_data != self._form_data:
            response = messagebox.askyesnocancel("Unsaved Changes", "Do you want to save changes before creating a new form?")

            if response is None:
                return
            elif response:
                self._file_save()

        self.active_form.gp = None
        self.active_form.dentist = None
        self.active_form.optician = None
        self.active_form.schools = []

        self._file_path = None

        self._original_form_data = self._current_form_data()

    def _file_open(self):
        file_path = filedialog.askopenfilename(defaultextension=".form", filetypes=[("Form files", "*.form")])

        data = {}

        if file_path:
            with open(file_path, "r") as file:
                data = json.load(file)

        self.active_form.gp = form.Form.import_service_from_json(data.get("gp", {}))
        self.active_form.dentist = form.Form.import_service_from_json(data.get("dentist", {}))
        self.active_form.optician = form.Form.import_service_from_json(data.get("optician", {}))
        schools_data = data.get("schools", [])
        self.active_form.schools = [form.Form.import_service_from_json(school) for school in schools_data]

        self._file_path = file_path

        self._original_form_data = self._current_form_data()

    def _file_open_recent(self, file_path):
        """
            TODO need to finish
        """
        data = {}

        if file_path:
            with open(file_path, "r") as file:
                data = json.load(file)

        self.active_form.gp = form.Form.import_service_from_json(data.get("gp", {}))
        self.active_form.dentist = form.Form.import_service_from_json(data.get("dentist", {}))
        self.active_form.optician = form.Form.import_service_from_json(data.get("optician", {}))
        schools_data = data.get("schools", [])
        self.active_form.schools = [form.Form.import_service_from_json(school) for school in schools_data]

        self._file_path = file_path

        self._original_form_data = self._current_form_data()


    def _file_save(self):
        # changed json files to .form files as the extension is more explanatory
        # use an attribute for the file path and trigger the dialog when that attribute is None
        # that way if the attribute is not None it automatically saves (normal behaviour of a save command)

        if self._file_path is None:
            self._file_path = filedialog.asksaveasfilename(defaultextension=".form", filetypes=[("Form files", "*.form")])
        data = {}
        if self._file_path:
            data = {
                "gp": form.Form.export_service_to_json(self.active_form.gp),
                "dentist": form.Form.export_service_to_json(self.active_form.dentist),
                "optician": form.Form.export_service_to_json(self.active_form.optician),
                "schools": [form.Form.export_service_to_json(school) for school in self.active_form.schools],
            }

        self._save_dict_as_json(data, self._file_path)

        self._original_form_data = self._current_form_data()

    def _file_save_as(self):
        self._file_path = filedialog.asksaveasfilename(defaultextension=".form", filetypes=[("Form files", "*.form")])
        data = {}
        if self._file_path:
            data = {
                "gp": form.Form.export_service_to_json(self.active_form.gp),
                "dentist": form.Form.export_service_to_json(self.active_form.dentist),
                "optician": form.Form.export_service_to_json(self.active_form.optician),
                "schools": [form.Form.export_service_to_json(school) for school in self.active_form.schools],
            }

        self._save_dict_as_json(data, self._file_path)

        self._original_form_data = self._current_form_data()

    def _file_export(self):
        pass

    def _file_import(self):
        pass

    def _form_clear(self):
        self.active_form.gp = None
        self.active_form.dentist = None
        self.active_form.optician = None
        self.active_form.schools = []

        # Reset file path
        self._file_path = None

        self._original_form_data = self._current_form_data()

    def _form_copy(self):
        copied_gp = copy.deepcopy(self.active_form.gp)
        copied_dentist = copy.deepcopy(self.active_form.dentist)
        copied_optician = copy.deepcopy(self.active_form.optician)
        copied_schools = copy.deepcopy(self.active_form.schools)

        # Convert the copied data to a string
        copied_str = f"GP: {copied_gp}\nDentist: {copied_dentist}\nOptician: {copied_optician}\nSchools: {copied_schools}"

        # Put the string representation into the clipboard
        # ref: python.hotexamples.com/examples/tkinter/Tk/clipboard_clear/python-tk-clipboard_clear-method-examples.html
        root = Tk()
        root.clipboard_clear()
        root.clipboard_append(copied_str)
        root.update()
        root.destroy()

    def _form_preview(self):
        pass

    def _help_user_manual(self):
        pass

    def _help_version_info(self):
        pass

    def _current_form_data(self):
        return {
            'gp': self.active_form.gp,
            'dentist': self.active_form.dentist,
            'optician': self.active_form.optician,
            'schools': self.active_form.schools,
        }

    @property
    def active_form(self) -> form.Form:
        return self.select()