from __future__ import annotations

from tkinter import Frame, Menu

import application.gui.app as app
from application.data.service import Service
from application.data.postcode import Postcode
from application.data.form_container import FormInformation


def _service_info(service: Service):
    information = "    Name: %s\n" % service.name
    information += "    Address (1): %s\n" % service.address_line_1
    information += "    Address (2): %s\n" % service.address_line_2
    if service.email:
        information += "    Email: %s\n" % service.email
    if service.telephone:
        information += "    Tel: %s\n" % service.telephone
    information += "\n"
    return information


class Form(Frame, FormInformation):
    def __init__(self, master: app.App, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._boof = Frame(self, width=400, height=400)
        self._boof.pack()

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

    def _export_service_to_json(self, service: Service) -> dict:
        """
        Converts a service to a json representation of the service

        (replace inside the curly braces)
        """
        return {...: ...}

    def _import_service_from_json(self, service: dict) -> Service:
        """
        Converts a jsonified service to a service object

        """
        return Service(...)
