import application.postcodes.postcode as pc
from abc import ABC, abstractmethod
from typing import Collection


class DatabaseIntermediary(ABC):
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
        Method called when the database intermediary object is about to stop existing; i.e. when the program is about to close.
        Allows for intermediary to prepare any closing preparations that need to be done.
        If the database closure is not successful, then the close_db method will be called again. If this attempt does not work,
        the user will be given an error pop-up
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
    def get_postcode(self, postcode: str) -> pc.Postcode | pc.Postcode.POSTCODE_NOT_EXIST:
        """
        Should return a postcode which exactly matches the given postcode, this postcode will be given
        using only alphanumeric characters (no spaces)
        
        :return: a postcode object
        """