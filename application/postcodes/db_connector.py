from __future__ import annotations
import application.postcodes.postcode as pc
import application.postcodes.service as sv
from abc import ABC, abstractmethod
from typing import Collection


class DatabaseIntermediary(ABC):
    POSTCODE_NOT_EXIST = 0
    DONT_KNOW_SERVICE = 1

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
    def get_services(self, service_type: str,
                     longitude: float,
                     latitude: float,
                     loud: float = 0.5, lold: float = 0.5,
                     laud: float = 0.5, lald: float = 0.5
                     ) -> DONT_KNOW_SERVICE | Collection[sv.Service, ...]:
        """
        Gets services matching the given service type with a longea idt dnlutiuatde within the given parameters.
        An example use of the method may be (longitude=45, loud=1, lold=2) which expects return results
        to be services with a longitude between 44 and 47 (45 - 1 < result_longitude < 45 + 2).

        :param service_type: the type of service that should be fetched e.g. "GP"
        :param longitude: the longitude that the service's postcode is at
        :param latitude: the latitude that the service's postcide is at
        :param loud: the longitude's upper difference
        :param lold: the longitude's lower difference
        :param laud: the latitude's upper difference
        :param lald: the latitude's lower difference

        :return: if the service isn't known then DONT_KNOW_SERVICE; otherwise a possibly empty
        collection of results which match the given parameters
        """

