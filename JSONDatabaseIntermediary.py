"""
I created this file because I needed an implementation of the database intermediary class for me to be able
to continue development on the GUI; otherwise I wouldn't be able to test any results. This will have to do
even if it is slow for the time being - Shaun
"""
from __future__ import annotations

from json import loads
from typing import Collection, Generator
from functools import cache

from application.data import service as sv, postcode as pc
from application.data.db_connector import DatabaseIntermediary


def objectify_postcode(plain: str, postcode: dict) -> pc.Postcode:
    return pc.Postcode(plain, postcode["longitude"], postcode["latitude"])


def objectify_service(service: dict, postcode: pc.Postcode) -> sv.Service:
    if isinstance(service["address"], list):
        address = [", ".join(service["address"][:1]), ", ".join(service["address"][1:])]
    else:
        address = service["address"].split(", ")
    addr1 = address[0]
    addr2 = addr1[1:]
    return sv.Service(postcode, service["name"], addr1, addr2, service["email"], service["telephone"], service["type"].upper())


class JSONDatabaseIntermediary(DatabaseIntermediary):
    def add_service(self, service: sv.Service):
        pass

    def add_postcode(self, postcode: pc.Postcode) -> DatabaseIntermediary.POSTCODE_EXIST | None:
        pass

    def update_service(self, service: sv.Service, name: str, email: str, phonenumber: int) -> sv.Service:
        pass

    def del_postcode(self, postcode: pc.Postcode) -> DatabaseIntermediary.POSTCODE_NOT_EXIST | DatabaseIntermediary.FAILED_TO_DELETE | None:
        pass

    def del_service(self, service: sv.Service) -> DatabaseIntermediary.DONT_KNOW_SERVICE | DatabaseIntermediary.FAILED_TO_DELETE | None:
        pass

    def __init__(self):
        self._postcodes: dict = {}
        self._services: dict = {}

    def postcodes(self) -> Generator[pc.Postcode]:
        for postcode, fields in self._postcodes.items():
            yield objectify_postcode(postcode, fields)

    def services(self) -> Generator[sv.Service]:
        for postcode, services in self._services.items():
            for service in services:
                yield objectify_service(service, self.get_postcode(postcode))

    def init_db(self) -> bool:
        with open("resources/ll-postcodes.json") as file:
            self._postcodes: dict = loads(file.read())

        with open("resources/services-info.json") as file:
            self._services: dict = loads(file.read())

        return bool(len(self._postcodes) and len(self._services))

    def close_db(self) -> bool:
        self._postcodes.clear()
        self._services.clear()
        return True

    @property
    def is_connected(self) -> bool:
        return True

    @property
    def command_able(self) -> bool:
        return bool(len(self._postcodes) and len(self._services))

    @cache
    def get_all_postcodes(self, outcode: str | None = None) -> Collection[pc.Postcode, ...]:
        return [postcode for postcode in self._postcodes.values() if postcode.startswith(outcode)]

    @cache
    def get_postcode(self, postcode: str) -> pc.Postcode | DatabaseIntermediary.POSTCODE_NOT_EXIST:
        if postcode in self._postcodes:
            return objectify_postcode(postcode, self._postcodes[postcode])
        else:
            return DatabaseIntermediary.POSTCODE_NOT_EXIST

    @cache
    def get_services(self,
                     service_type: str,
                     longitude: float,
                     latitude: float,
                     distance: float,
                     distance_from_postcode: pc.Postcode | None = None,
                     distance_from_coordinates: tuple[float, float] | None = None,
                     max_number=0
                     ) -> DatabaseIntermediary.DONT_KNOW_SERVICE | Collection[sv.Service, ...]:
        """

        """
        services_found = []
        if distance_from_postcode is not None:
            def check_distance(_postcode: pc.Postcode):
                return _postcode.distance_between(distance_from_postcode) < distance
        else:
            def check_distance(_postcode: pc.Postcode):
                return _postcode.distance_between(pc.Postcode("", *distance_from_coordinates)) < distance
        if max_number >= 1:
            for postcode, services in self._services.items():
                if len(services_found) == max_number:
                    break
                postcode_obj = self.get_postcode(postcode)
                if postcode_obj == DatabaseIntermediary.POSTCODE_NOT_EXIST:
                    continue
                if check_distance(postcode_obj):
                    for service in services:
                        if len(services_found) == max_number:
                            break
                        service["type"].upper() == service_type and services_found.append(objectify_service(service, postcode_obj))
        else:
            for postcode, services in self._services.items():
                postcode_obj = self.get_postcode(postcode)
                if postcode_obj == DatabaseIntermediary.POSTCODE_NOT_EXIST:
                    continue
                if check_distance(postcode_obj):
                    for service in services:
                        service["type"].upper() == service_type and services_found.append(objectify_service(service, postcode_obj))
        return services_found
