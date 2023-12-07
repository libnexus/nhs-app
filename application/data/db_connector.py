from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Collection

import application.data.postcode as pc
import application.data.service as sv


class DatabaseIntermediary(ABC):
    POSTCODE_NOT_EXIST = 0
    DONT_KNOW_SERVICE = 1
    POSTCODE_EXIST = 2
    FAILED_TO_DELETE = 3

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def init_db(self) -> bool:
        """
        Mehtod called to inintialize the database intermediary object and any of it's related objects.
        Should be invoked on program start up.
        If the initialization was successful then the object will continue to exist, otherwise the intermediary
        object will be deleted and another intermediary object will be created; if 5 attempts refuse to connect
        then a user error pop-up will appear
        Because this method should return a true or false value, the method is required to not allow
        any errors to propagate further than the closure of the method.
        
        :return: if the database initialization was successful then true should be returned otherwise false
        """

    @abstractmethod
    def close_db(self) -> bool:
        """
        Method called when the database intermediary object is about to stop existing; i.e. when the program is about to
        close.
        Allows for intermediary to prepare any closing preparations that need to be done.
        If the database closure is not successful, then the close_db method will be called again. If this attempt does
        not work, the user will be given an error pop-up
        Because this method should return a true or false value, the method is required to not allow
        any errors to propagate further than the closure of the method.
        
        :return: if the database closure was successful then true should be returned otherwise false
        """

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Simple getter method for checking if the database's connection is still active and therefore still
        able to process any requests which should return either True for able to process commands or False
        for not able to process commands. Even if this object is able to process commands, if it is not connected
        to the database it should still return false as this method cares about connection

        :return: a boolean; either True for connected or False for not connected
        """

    @property
    @abstractmethod
    def command_able(self) -> bool:
        """
        Simple getter method for checking if this object is able to process commands as though it has a
        connection to the database even if it does not have an active connection. This allows the object to
        implement any number of caching strategies for it's method results for assumed use

        :return: a boolean; either True for able to process commands or False for unable to process commands
        """

    @abstractmethod
    def get_all_postcodes(self, outcode: str | None = None) -> Collection[pc.Postcode, ...]:
        """
        Should return a collection of all postcode objects available to the databse which begin with
        a given outcode.
        The outcode given as an argument is meant to allow the searching function to filter any objects
        which don't start with the given outcode if any.
        
        :param outcode: the outcode component of the postcode which will be no more than 4 characters
        
        :return: some collection of postcode objects 
        """

    @abstractmethod
    def get_postcode(self, postcode: str) -> pc.Postcode | POSTCODE_NOT_EXIST:
        """
        Should return a postcode which exactly matches the given postcode, this postcode will be given
        using only alphanumeric characters (no spaces)
        
        :param postcode: the postcode string to get a postcode object of, will have no spaces

        :return: a postcode object
        """

    @abstractmethod
    def get_services(self,
                     service_type: str,
                     postcode: pc.Postcode,
                     distance: float,
                     ) -> DONT_KNOW_SERVICE | Collection[sv.Service, ...]:
        """
        Gets services matching the given service type with a longea idt dnlutiuatde within the given parameters.
        An example use of the method may be (longitude=45, loud=1, lold=2) which expects return results
        to be services with a longitude between 44 and 47 (45 - 1 < result_longitude < 45 + 2).

        :param service_type: the type of service that should be fetched e.g. "GP"
        :param postcode: the postcode to judge distance from
        :param distance: the farthest distance (modifies longitude and latitude)  from either the given postcode or coordinates

        :return: if the service isn't known then DONT_KNOW_SERVICE; otherwise a possibly empty
        collection of results which match the given parameters
        """

    
    """vvv Ricardo vvv"""

    @abstractmethod
    def add_service(self, service: sv.Service):
        """
        
        Adds new service to the database

        :param service: the service to be added to the database

        """
    
    @abstractmethod
    def add_postcode(self, postcode: pc.Postcode) -> POSTCODE_EXIST | None:
        """
        
        Adds new postcode to the database
        Should check if entered postcode is a duplicate, if so return POSTCODE_EXIST 

        :param postcode: the postcode to be added to the database
        :return: an error if postcode exists, else nothing

        """


    @abstractmethod
    def update_service(self, service: sv.Service, name: str, email: str, phonenumber: int) -> sv.Service:
        """

        can change the name, email, and/or phone number of an existing service, and updates the database externally.

        :param service: the service to be updated
        :return: returns new service object
        
        """

    @abstractmethod
    def del_postcode(self, postcode: pc.Postcode) -> POSTCODE_NOT_EXIST | FAILED_TO_DELETE | None:
        """
        
        deletes existing postcode, returns error if the task was not able to be executed, or if postcode doesnt exist

        :param postcode: postcode to be deleted
        :return: returns error if postcode doesnt exist or it failed, else nothing

        """

    @abstractmethod
    def del_service(self, service: sv.Service) -> DONT_KNOW_SERVICE | FAILED_TO_DELETE | None:
        """
        deletes existing service, returns error if the task was not able to be executed, or if service doesnt exist

        :param service: service to be deleted
        :return: returns error if service doesnt exist or it failed, else nothing

        """
    
    """^^^ Ricardo ^^^"""

    @abstractmethod
    def get_service_by_name(self, name: str) -> sv.Service:
        """
        gets an existing service by it's name, if there is no service with a suitable name stored then returns an error

        :param name: the name of the service to get
        :return: the service object or an error if there's no name
        """