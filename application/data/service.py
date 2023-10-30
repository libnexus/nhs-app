from __future__ import annotations
from functools import cache
from typing import Collection
import application.data.postcode as pc


class Service:
    """
    The service object returned by a database intermediary method
    """
    
    @staticmethod
    def sort_by_distance(postcode: pc.Postcode, services: Collection[Service, ...]) -> tuple[Service, ...]:
        differences = {}
        for service in services:
            diff = postcode.distance_between(service.postcode)
            if diff in differences:
                differences[diff].append(service)
            else:
                differences[diff] = [service]

        sorted_differences = []
        for sk in sorted(differences.keys()):
            sorted_differences.extend(differences[sk])

        return tuple(sorted_differences)

    @cache 
    def __new__(cls,
                postcode: pc.Postcode,
                name: str,
                address_line_1: str,
                address_line_2: str,
                email: str,
                service_type: str):
        """
        Simple method override for the __new__ in order to cache service object
        creation which helps reserve memory.

        :return: either a new or cached service object
        """
        
    def __init__(self,
                 postcode: pc.Postcode,
                 name: str,
                 address_line_1: str,
                 address_line_2: str,
                 email: str,
                 service_type: str):
        """
        Initializer method to create private fields for the service object
        
        :param postcode: a postcode object for where the service exists
        :param name: the name of the service e.g. "Randstad"
        :param address_line_1: the first line of the full address of the service; shouldn't be empty
        :param address_line_2: the second line of the full address of the service; may be empty
        :param email: an email address if available for the service; may be empty
        :param service_type: a service type, written as a database intermediary may find it e.g. "SCHOOL";
        should be in all caps
        """
        self._postcode = postcode
        self._name = name
        self._address_line_1 = address_line_1
        self._address_line_2 = address_line_2
        self._email = email
        self._service_type = service_type
    
    @property
    def postcode(self) -> pc.Postcode:
        """
        The postcode object for where the service exists in an area
        
        :return: a postcode object
        """
        return self._postcode
    
    @property
    def name(self):
        """
        The name of the service as it is to be addressed
        
        :return: the name as a string
        """
        return self._name
    
    @property
    def address_line_1(self):
        """
        The first line of the full address of the service which will not be an empty string
        
        :return: a non-empty string, the first line of the address of the service
        """
        return self._address_line_1
        
    @property
    def address_line_2(self):
        """
        The second line of the full address of the service which may be an empty string
        
        :return: a possibly empty string, the second line of the adress of the service
        """
        return self._address_line_2
        
    @property
    def email(self):
        """
        The email of the service if available that can be used to contact the main service
        
        :return: a possibly empty string, the email of the service
        """
        return self._email
    
    @property
    def service_type(self):
        """
        The type of service that the service object represents, which should be expected to be: "SCHOOL-NURSERY",
        "GP", "OPTICIAN", "DENTIST" or any other type which may be supported in future. It will not be empty
        
        :return: a string, the type of service in all caps
        """
        return self._service_type
