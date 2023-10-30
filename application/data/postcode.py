from __future__ import annotations 
from functools import cache
from math import pi, sin, cos, atan2, sqrt


class Postcode:
    """
    The postcode object returned by a database intermediary method
    """

    @cache
    def __new__(cls, postcode: str, longitude: float, latitude: float) -> Postcode:
        """
        Simple method override for the __new__ in order to cache postcode object
        creation which helps reserve memory and allows other methods which expect
        postcode objects to be cached to operate predictably.

        :return: either a new or cached postcode object
        """
        return super().__new__(cls)

    def __init__(self, postcode: str, longitude: float, latitude: float):
        """
        Initializer method to create private fields for the postcode object.

        :param postcode: the plain text postcode for the postcode object
        :param longitude: the longitudinal coordinate that the postcode occupies
        :param latitude: the latitudinal coordinate the postcode occupies
        """
        self._postcode = postcode
        self._longitude = longitude
        self._latitude = latitude

    @property
    def postcode(self) -> str:
        """
        The string postcode of the postcode object which will be formatted with no spaces, only
        alphanumeric characters

        :return: the plain text postcode
        """
        return self._postcode

    @property
    def nice_postcode(self) -> str:
        """
        The string postcode of the postcode object formatted with a space between the outcode
        and incode

        :return: the postcode formatted
        """
        return self._postcode[:4] + " " + self._postcode[4:]

    @property
    def longitude(self) -> float:
        """
        The longitudinal coordinate that the postcode occupies on earth

        :return: the longitude; a float
        """
        return self._longitude

    @property
    def latitude(self) -> float:
        """
        The latitudinal coordinate that the postcode occupies on earth

        :return: the latitude; a float
        """
        return self._latitude

    @cache
    def distance_between(self, other: Postcode) -> float:
        """
        Uses the haversine formula to calculate the unobstructed "bird's eye view" distance between
        two data over the surface of the earth as a globular entity.
        An implementation of the code provided from https://www.movable-type.co.uk/scripts/latlong.html

        :param other: the other postcode to compare the distance between
        :return: the distance between the two data measured in metres
        """
        return self._distance_between(self.longitude, self.latitude, other.longitude, other.latitude)

    @staticmethod
    @cache
    def _distance_between(long1: float, lat1: float, long2: float, lat2: float):
        """
        Uses the haversine formula to calculate the unobstructed "bird's eye view" distance between
        two data over the surface of the earth as a globular entity.
        An implementation of the code provided from https://www.movable-type.co.uk/scripts/latlong.html

        :param long1: the first postcode's longitude
        :param lat2: the first postcode's latitude
        :param long2: the second postcode's longitude
        :param lat2: the second postcode's latitude
        :return: the distance between the two data measured in metres
        """
        phi1 = (lat1 * pi / 180)
        phi2 = (lat2 * pi / 180)
        delta_phi = ((lat2 - lat1) * pi / 180)
        delta_lambda = ((long2 - long1) * pi / 180)
        a = sin(delta_phi / 2) * sin(delta_phi / 2) + \
            cos(phi1) * cos(phi2) * sin(delta_lambda / 2) * sin(delta_lambda / 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))  # angular distance in radians
        return 6371e3 * c  # the radius of the earth in metres
