from __future__ import annotations

from tkinter import Frame
from typing import Collection

from application.data import postcode as pc, service as sv
from application.data.form_container import FormInformation
from application.data.postcode import Postcode
from application.data.service import Service
import application.data.persistent_storage as pss

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

    def __init__(self, master, postcode: Postcode, *args, **kwargs):
        super(Frame).__init__(master, *args, **kwargs)
        super(FormInformation).__init__()

        self._postcode: Postcode = postcode
        self._gp: Service | None = None
        self._dentist: Service | None = None
        self._optician: Service | None = None
        self._schools: list[Service, ...] = []

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
