from __future__ import annotations

from tkinter import Frame, messagebox
from typing import Collection

from application.data import postcode as pc, service as sv
from application.data.form_container import FormInformation
from application.data.postcode import Postcode
from application.data.service import Service
from application.gui.service_info_entry import ServiceInformationEntry
from application.gui.service_listbox import ServiceListbox
import application.data.persistent_storage as pss
import application.data.db_connector as db
from tkinter import LabelFrame, Button, Menu
from tkinter.filedialog import asksaveasfile


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

        if pss.AppConfig.get_colour_theme("default"):
            self.config(background="white")
        elif pss.AppConfig.get_colour_theme("dark"):
            self.config(background="grey")

    def __init__(self, master, postcode: Postcode, database_intermediary: db.DatabaseIntermediary, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        FormInformation.__init__(self)

        self._database_intermediary = database_intermediary

        self._postcode: Postcode = postcode
        self._gp: Service | None = None
        self._dentist: Service | None = None
        self._optician: Service | None = None
        self._schools: list[Service] = []

        self.winfo_toplevel().title("Service selection form for %s" % self._postcode.nice_postcode)
        self.update()

        self._gp_select_frame = LabelFrame(self, text="Select GP")
        if pss.AppConfig.get_colour_theme("default"):
            self._gp_select_frame.config(background="white")
        elif pss.AppConfig.get_colour_theme("dark"):
            self._gp_select_frame.config(background="grey")
            self._gp_submit_button = Button(self._gp_select_frame, text="Select",
                                        command=self._select_service("GP", "_gp_submit_button"),
                                        width=20)
        if pss.AppConfig.get_colour_theme("default"):
            self._gp_submit_button.config(background="light blue")
        self._gp_submit_button.pack(padx=10, pady=10)
        self._gp_select_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self._dentist_select_frame = LabelFrame(self, text="Select Dentist")
        if pss.AppConfig.get_colour_theme("default"):
            self._dentist_select_frame.config(background="white")
        elif pss.AppConfig.get_colour_theme("dark"):
            self._dentist_select_frame.config(background="grey")
        self._dentist_submit_button = Button(self._dentist_select_frame, text="Select",
                                             command=self._select_service("DENTIST",
                                                                          "_dentist_submit_button"),
                                             width=20)
        if pss.AppConfig.get_colour_theme("default"):
            self._dentist_submit_button.config(background="light blue")
        self._dentist_submit_button.pack(padx=10, pady=10)
        self._dentist_select_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self._optician_select_frame = LabelFrame(self, text="Select Optician")
        if pss.AppConfig.get_colour_theme("default"):
            self._optician_select_frame.config(background="white")
        elif pss.AppConfig.get_colour_theme("dark"):
            self._optician_select_frame.config(background="grey")
        self._optician_submit_button = Button(self._optician_select_frame, text="Select",
                                              command=self._select_service("OPTICIAN",
                                                                           "_optician_submit_button"),
                                              width=20)
        if pss.AppConfig.get_colour_theme("default"):
            self._optician_submit_button.config(background="light blue")
        self._optician_submit_button.pack(padx=10, pady=10)
        self._optician_select_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self._school_view = None

        def _schools_view():
            if self._school_view is None:
                self._school_view_frame = LabelFrame(self, text="Selected Schools (Double click to remove)")
                if pss.AppConfig.get_colour_theme("default"):
                    self._school_view_frame.config(background="white")
                elif pss.AppConfig.get_colour_theme("dark"):
                    self._school_view_frame.config(background="grey")
                self._school_view = ServiceListbox(self._school_view_frame, self._del_school, width=10)
                if pss.AppConfig.get_colour_theme("default"):
                    self._school_view.config(background="white")
                elif pss.AppConfig.get_colour_theme("dark"):
                    self._gp_submit_button.config(background="grey")
                self._school_view.pack()
                self._school_view_frame.grid(row=0, column=2, padx=10, pady=10, rowspan=2)
            self._add_school()

        self._add_school_frame = LabelFrame(self, text="Select School")
        if pss.AppConfig.get_colour_theme("default"):
            self._add_school_frame.config(background="white")
        elif pss.AppConfig.get_colour_theme("dark"):
            self._gp_submit_button.config(background="grey")
        self._add_school_button = Button(self._add_school_frame, text="Select",
                                         command=_schools_view,
                                         width=20)
        if pss.AppConfig.get_colour_theme("default"):
            self._add_school_frame.config(background="light blue")
        self._add_school_button.pack(padx=10, pady=10)
        self._add_school_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Will move for final

        self._menu = Menu(self)
        self._menu.add_command(label="Export", command=self._export)
        self.winfo_toplevel().config(menu=self._menu)

    def _export(self):
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
        file.write(text)
        file.close()
        messagebox.showinfo("Success!", "The file was successfully saved")

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
