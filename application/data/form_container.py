from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Collection

import application.data.postcode as pc
import application.data.service as sv


class FormInformation(ABC):
    @property
    @abstractmethod
    def gp(self) -> sv.Service:
        """
        The current GP that the form has stored as user choice

        :return: a service of the "GP" type
        """

    @property
    @abstractmethod
    def optician(self) -> sv.Service:
        """
        The current optician that the form has stored as user choice

        :return: a service of the "OPTICIAN" type
        """

    @property
    @abstractmethod
    def dentist(self) -> sv.Service:
        """
        The current dentist that the form has stored as user choice

        :return: a service of the "DENTIST" type
        """

    @property
    @abstractmethod
    def schools(self) -> Collection[sv.Service, ...]:
        """
        The current GP that the form has stored as user choice

        :return: a service of the "GP" type
        """

    @property
    @abstractmethod
    def postcode(self) -> pc.Postcode:
        """
        The current postcode for which this form container is a reference to selections from

        :return: a postcode
        """