from __future__ import annotations

from json import loads, dumps
from tkinter import Frame, messagebox
from tkinter import LabelFrame, Button, Menu
from tkinter.filedialog import asksaveasfile, askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno
from typing import Collection

import application.data.db_connector as db
import application.data.persistent_storage as pss
import application.gui.colour as colour
import application.gui.postcode_entry as pce
from application.data import postcode as pc, service as sv
from application.data.form_container import FormInformation
from application.data.postcode import Postcode
from application.data.service import Service
from application.gui.service_info_entry import ServiceInformationEntry
from application.gui.service_listbox import ServiceListbox


def _service_info(service: Service):
    information = "    Name: %s\n" % service.name
    information += "    Address (1): %s\n" % service.address_line_1
    if service.address_line_2:
        information += "            (2): %s\n" % service.address_line_2
    if service.email:
        information += "    Email: %s\n" % service.email
    if service.telephone:
        information += "    Tel: %s\n" % service.telephone
    information += "\n"
    return information


class ServicePreviewFrame(LabelFrame):
    def __init__(self, master, service: Service, click, *args, **kwargs):
        super().__init__(master, *args, text=service.name_truncated, **kwargs)
        self.service = service
        self.bind("<Double-Button-1>", lambda e: click(self))


class Form(Frame, FormInformation):
    @property
    def gp(self) -> sv.Service:
        return self._gp

    @property
    def optician(self) -> sv.Service:
        return self._optician

    @property
    def dentist(self) -> sv.Service:
        return self._dentist

    @property
    def schools(self) -> Collection[sv.Service, ...]:
        return self._schools

    @property
    def postcode(self) -> pc.Postcode:
        return self._postcode

    def service_info(self,
                     gp: Service | None = None,
                     dentist: Service | None = None,
                     optician: Service | None = None,
                     schools: Collection[Service, ...] | None = None):
        """
        Sets the services of the form. Uses keyword arguments.

        :param gp: the new gp to set
        :param dentist: the new dentist to set
        :param optician: the new optician to set
        :param schools: the new schools to set
        """
        if gp:
            self._gp = gp
        if dentist:
            self._dentist = dentist
        if optician:
            self._optician = optician
        if schools:
            self._schools = schools

    def __init__(self, master, postcode: Postcode, database_intermediary: db.DatabaseIntermediary, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        FormInformation.__init__(self)

        self._database_intermediary = database_intermediary

        self._postcode: Postcode = postcode
        self._gp: Service | None = None
        self._dentist: Service | None = None
        self._optician: Service | None = None
        self._schools: list[Service] = []

        self._form_data = self._current_form_data()

        self.winfo_toplevel().title("Service selection form for %s" % self._postcode.nice_postcode)
        self.update()

        self._gp_select_frame = LabelFrame(self, text="Select GP")
        self._gp_select_frame.config(background=colour.COLOUR.medium)
        self._gp_submit_button = Button(self._gp_select_frame, text="Select",
                                        command=self._select_service("GP", "_gp_submit_button"),
                                        width=20)
        self._gp_submit_button.config(background=colour.COLOUR.light)
        self._gp_submit_button.pack(padx=10, pady=10)
        self._gp_select_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self._dentist_select_frame = LabelFrame(self, text="Select Dentist")
        self._dentist_select_frame.config(background=colour.COLOUR.medium)
        self._dentist_submit_button = Button(self._dentist_select_frame, text="Select",
                                             command=self._select_service("DENTIST",
                                                                          "_dentist_submit_button"),
                                             width=20)
        self._dentist_submit_button.config(background=colour.COLOUR.light)
        self._dentist_submit_button.pack(padx=10, pady=10)
        self._dentist_select_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self._optician_select_frame = LabelFrame(self, text="Select Optician")
        self._optician_select_frame.config(background=colour.COLOUR.medium)
        self._optician_submit_button = Button(self._optician_select_frame, text="Select",
                                              command=self._select_service("OPTICIAN",
                                                                           "_optician_submit_button"),
                                              width=20)
        self._optician_submit_button.config(background=colour.COLOUR.light)
        self._optician_submit_button.pack(padx=10, pady=10)
        self._optician_select_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self._school_view: None | ServiceListbox = None
        self._school_view_frame: None | Frame = None

        def truncate(string: str, places: int, suffix: str = "...") -> str:
            if len(string) < places + len(suffix):
                return string
            else:
                return string[:len(suffix)] + suffix

        def _schools_view():
            if self._school_view is None:
                self._school_view_frame = LabelFrame(self, text="Selected Schools (Double click to remove)")
                self._school_view_frame.config(background=colour.COLOUR.medium)
                self._school_view = ServiceListbox(self._school_view_frame, self._del_school, width=10)
                self._school_view.config(background=colour.COLOUR.medium)
                self._school_view.pack()
                self._school_view_frame.grid(row=0, column=2, padx=10, pady=10, rowspan=2)
            self._add_school()

        self._add_school_frame = LabelFrame(self, text="Select School")
        self._add_school_frame.config(background=colour.COLOUR.medium)
        self._add_school_button = Button(self._add_school_frame, text="Select",
                                         command=_schools_view,
                                         width=20)
        self._add_school_button.config(background=colour.COLOUR.light)
        self._add_school_button.pack(padx=10, pady=10)
        self._add_school_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Will move for final
        self._file_path = None

        self._menu = Menu(self)

        file_menu = Menu(self._menu, tearoff=0)
        file_menu.add_command(label="New", command=self._file_new)
        file_menu.add_command(label="Open", command=self._file_open)
        # ref: https://coderslegacy.com/python/create-submenu-in-tkinter/
        recent_menu = Menu(self._menu, tearoff=0)

        file_menu.add_cascade(label="Open recent", menu=recent_menu)
        for i, path in enumerate(pss.AppConfig.get_recent_files()):
            recent_menu.add_command(label="%d. %s" % (i, truncate(path, 10)))

        file_menu.add_command(label="Save", command=self._file_save)
        file_menu.add_command(label="Save As", command=self._file_save_as)
        file_menu.add_command(label="Export", command=self._file_export)
        file_menu.add_separator()
        # Added exit option in menu, not needed but nice addition
        file_menu.add_command(label="Exit", command=self.quit)
        self._menu.add_cascade(label="File", menu=file_menu)

        form_menu = Menu(self._menu, tearoff=0)
        form_menu.add_command(label="Clear", command=self._file_new)
        form_menu.add_command(label="Copy", command=self._form_copy)
        form_menu.add_separator()
        self._menu.add_cascade(label="Form", menu=form_menu)

        help_menu = Menu(self._menu, tearoff=0)
        help_menu.add_command(label="Version Info", command=self._help_version_info)
        self._menu.add_cascade(label="Help", menu=help_menu)

        self.winfo_toplevel().config(menu=self._menu)

        self._recent_menu = recent_menu
        self._file_menu = file_menu
        self._form_menu = form_menu
        self._help_menu = help_menu

    def _file_open(self):
        if not askyesno("Are you sure?",
                        "If you open a new file, your form will be overwritten. Are you sure you want to continue?"):
            return

        file_path = askopenfilename(defaultextension=".form", filetypes=[("Form files", "*.form")])

        if file_path:
            with open(file_path, "r") as file:
                data = loads(file.read())
        else:
            return

        self._form_data = self._current_form_data()

    def _file_new(self):
        if self._current_form_data() is not self._form_data:
            response = messagebox.askyesnocancel("Unsaved Changes",
                                                 "Your form will be overwritten. "
                                                 "Do you want to save changes before creating a new form? ")

            if response:
                self._file_save()

        def get_postcode(_postcode):
            self._postcode = _postcode
            self._gp = None
            self._dentist = None
            self._optician = None
            self._schools = []

            self._file_path = "."
            self._form_data = self._current_form_data()

            self._gp_submit_button.config(text="Select")
            self._dentist_submit_button.config(text="Select")
            self._optician_submit_button.config(text="Select")
            if self._school_view:
                self._school_view.destroy()
                self._school_view = None
                self._school_view_frame.destroy()
                self._school_view_frame = None
            self.winfo_toplevel().title("Service selection form for %s" % _postcode.nice_postcode)

        pce.PostcodeEntry(self.winfo_toplevel(), self._database_intermediary, get_postcode)

        self._form_data = self._current_form_data()

    def _file_save(self):
        """
            changed json files to .form files as the extension is more explanatory
            use an attribute for the file path and trigger the dialog when that attribute is None
            that way if the attribute is not None it automatically saves (normal behaviour of a save command)
                """

        if self._file_path is None:
            _file_path = asksaveasfilename(defaultextension=".form", filetypes=[("Form files", "*.form")])
            if _file_path:
                self._file_path = _file_path
            else:
                return

        data = {}
        if self._file_path:
            data = {
                "gp": self.export_service_to_json(self.gp) if self.gp is not None else None,
                "dentist": self.export_service_to_json(self.dentist) if self.dentist is not None else None,
                "optician": self.export_service_to_json(self.optician) if self.optician is not None else None,
                "schools": [self.export_service_to_json(school) for school in self.schools],
            }

        self._save_dict_as_json(data, self._file_path)
        self._form_data = self._current_form_data()
        messagebox.showinfo("Success!", "The file was successfully saved")

    def _file_save_as(self):
        self._file_path = asksaveasfilename(defaultextension=".form", filetypes=[("Form files", "*.form")])

        data = {}
        if self._file_path:
            data = {
                "gp": self.export_service_to_json(self.gp) if self.gp is not None else "",
                "dentist": self.export_service_to_json(self.dentist) if self.dentist is not None else "",
                "optician": self.export_service_to_json(self.optician) if self.optician is not None else "",
                "schools": [self.export_service_to_json(school) for school in self.schools],
            }

        self._save_dict_as_json(data, self._file_path)
        self._form_data = self._current_form_data()
        messagebox.showinfo("Success!", "The file was successfully saved")

    def _save_dict_as_json(self, data: dict, file_path: str):
        with open(file_path, "w") as file:
            file.write(dumps(data))

    def _file_export(self):
        text = ""

        if self._gp:
            text += "\nGP:\n" + _service_info(self._gp) + "\n"

        if self._optician:
            text += "\nOptician:\n" + _service_info(self._optician) + "\n"

        if self._dentist:
            text += "\nDentist:\n" + _service_info(self._dentist) + "\n"

        if self.schools:
            text += "\nSchools:\n"
            for school in self.schools:
                text += "\n" + _service_info(school) + "\n"

        file = asksaveasfile(mode='w', initialfile="%s - %s" % (self.postcode.nice_postcode, id(self)),
                             filetypes=[("Form files", "*.form"), ("Text files", "*.txt")])
        file.write(text.lstrip())
        file.close()
        messagebox.showinfo("Success!", "The file was successfully exported")

    def _help_version_info(self):
        messagebox.showinfo("Version info",
                            "Application version: V2.0\n"
                            "Developer names: Shaun Cameron, Ynyr Elis-Davies, Cameron Brown, Ricardo De Jesus\n"
                            "Release date: 14/12/2023")

    def _form_copy(self):
        # Put the string representation into the clipboard
        # ref: python.hotexamples.com/examples/tkinter/Tk/clipboard_clear/python-tk-clipboard_clear-method-examples.html
        self.winfo_toplevel().clipboard_clear()
        self.winfo_toplevel().clipboard_append(dumps({
            "gp": self.export_service_to_json(self.gp) if self.gp is not None else None,
            "dentist": self.export_service_to_json(self.dentist) if self.dentist is not None else None,
            "optician": self.export_service_to_json(self.optician) if self.optician is not None else None,
            "schools": [self.export_service_to_json(school) for school in self.schools],
        }))

    def _del_school(self, service: Service, widget: Frame):
        self._schools.remove(service)
        widget.destroy()

    def _add_school(self):
        def __add_school__(school: Service):
            self._schools.append(school)
            self._school_view.add_new_service(school)
            self._school_view.update()

        ServiceInformationEntry(self, self._postcode, "SCHOOL", self._database_intermediary, __add_school__)

    def _select_service(self, service_type: str, button: str):
        def __select_service__():
            def ___select_service___(_service: Service):
                setattr(self, "_%s" % service_type.lower(), _service)
                getattr(self, button).config(text=_service.name_truncated)

            ServiceInformationEntry(self, self._postcode, service_type, self._database_intermediary,
                                    ___select_service___)

        return __select_service__

    def _select_gp(self):
        def __select_gp__(gp: Service):
            self._gp = gp
            self._gp_submit_button.config(text=self._gp.name_truncated)

        ServiceInformationEntry(self, self._postcode, "GP", self._database_intermediary, __select_gp__)

    def _compile_information_to_string(self) -> str:
        """
        Compiles the information given into a nice string which can then be exported to a txt file
        Modifications to this method may make it compile to html which can be converted to pdf
        """
        information = ""

        for name, service in zip(["GP", "Dentist", "Optician"], [self._gp, self._dentist, self._optician]):
            information += "Information for %s\n" % name
            information += _service_info(service)

        for i, school in enumerate(self._schools):
            information += "Child %ds school:" % i
            information += _service_info(school)

        return information

    def _current_form_data(self):
        return {
            'gp': self.gp,
            'dentist': self.dentist,
            'optician': self.optician,
            'schools': self.schools,
        }

    @staticmethod
    def export_service_to_json(service: Service) -> dict:
        """
        Converts a service to a json representation of the service

        """
        return {
            "postcode": service.postcode.postcode,
            "name": service.name,
            "address_line_1": service.address_line_1,
            "address_line_2": service.address_line_2,
            "email": service.email,
            "telephone": service.telephone,
            "service_type": service.service_type,
        }

    @staticmethod
    def import_service_from_json(service: dict) -> Service:
        """
        Converts a json representation of a service to a service object

        """
        postcode = Postcode(service.get("postcode", ""))
        name = service.get("name", "")
        address_line_1 = service.get("address_line_1", "")
        address_line_2 = service.get("address_line_2", "")
        email = service.get("email", "")
        telephone = service.get("telephone", "")
        service_type = service.get("service_type", "")

        return Service(postcode=postcode, name=name, address_line_1=address_line_1, address_line_2=address_line_2,
                       email=email, telephone=telephone, service_type=service_type)
