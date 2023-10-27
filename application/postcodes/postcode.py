from __future__ import annotations 
from functools import cache
from math import pi, sin, cos, atan2, sqrt


class Postcode:
    """
    The postcode object returned by a database intermediary method
    """

    POSTCODE_NOT_EXIST = 0

    @cache
    def __new__(cls, postcode: str, longitude: float, latitude: float):
        """
        Simple method override for the __new__ in order to cache postcode object
        creation which helps reserve memory and allows other methods which expect
        postcode objects to be cached to operator predictably.

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
        two postcodes over the surface of the earth as a globular entity.
        An implementation of the code provided from https://www.movable-type.co.uk/scripts/latlong.html

        :param other: the other postcode to compare the distance between
        :return: the distance between the two postcodes measured in metres
        """
        a = self._distance_between_for_a(other)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))  # angular distance in radians
        return 6371e3 * c  # the radius of the earth in metres multiplied by c

    def _distance_between_for_a(self, other: Postcode):
        """
        :param other: the other postcode being used in the main distance_between function
        :return: the calculated value for "a" (the square of half the chord length between the two points on the globe)
        between this postcode and the other postocde
        """
        phi1 = (self.latitude * pi / 180)
        phi2 = (other.latitude * pi / 180)
        delta_phi = ((other.latitude - self.latitude) * pi / 180)
        delta_lambda = ((other.longitude - self.longitude) * pi / 180)
        return sin(delta_phi / 2) * sin(delta_phi / 2) + cos(phi1) * cos(phi2) * sin(delta_lambda / 2) * sin(delta_lambda / 2)
               
               
print(Postcode("", 0, 0))
