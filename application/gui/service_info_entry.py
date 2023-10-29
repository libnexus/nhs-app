from tkinter import Toplevel, Entry, Label, LabelFrame, Button, W, messagebox
from typing import Callable, Collection
import application.postcodes.postcode as pc
import application.postcodes.service as sv
import application.postcodes.db_connector as dbc
import re as regex


EMAIL_REGEX: regex.Pattern = ...
TELEPHONE_REGEX: regex.Pattern = ...


class ServiceInformationEntry(Toplevel):
    def __init__(self,
                 master,
                 postcode: pc.Postcode,
                 service_type: str,
                 database_connector: dbc.DatabaseIntermediary,
                 info_return_callback: Callable[[sv.Service], None]):
        """

        :param master: the widget / frame that this object is a slave of (belongs to/in)
        :param postcode: a postcode object to abse search results on
        :param service_type: the type of service that the information entry is responsible for returning
        :param database_connector: the database intermediary the service information entry should use
        to fetch results
        :param info_return_callback:
        """
        super().__init__(master)

        self._postcode = postcode 
        self._dbc = database_connector
        self._service_type = service_type
        self._irc = info_return_callback

        self._name_entry_frame = LabelFrame(self, text="Name")
        self._name_entry = Entry(self._name_entry_frame, width=40)
        self._name_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        self._address_entry_frame = LabelFrame(self, text="Address")
        self._postcode_label = Label(self._address_entry_frame, text="Postcode")
        self._postcode_entry = Entry(self._address_entry_frame, width=10)
        self._address_1_label = Label(self._address_entry_frame, text="Address Line 1")
        self._address_1_entry = Entry(self._address_entry_frame, width=60)
        self._address_2_label = Label(self._address_entry_frame, text="Address Line 2")
        self._address_2_entry = Entry(self._address_entry_frame, width=60)

        self._postcode_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self._postcode_entry.grid(row=0, column=1, padx=5, sticky=W)
        self._address_1_label.grid(row=1, column=0, padx=5)
        self._address_1_entry.grid(row=1, column=1, padx=5)
        self._address_2_label.grid(row=2, column=0, padx=5, pady=5)
        self._address_2_entry.grid(row=2, column=1, padx=5)

        self._email_entry_frame = LabelFrame(self, text="Email")
        self._email_entry = Entry(self._email_entry_frame, width=40)
        self._email_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        self._telephone_entry_frame = LabelFrame(self, text="Telephone")
        self._telephone_entry = Entry(self._telephone_entry_frame, width=40)
        self._telephone_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        self._name_entry_frame.grid(row=0, column=1, padx=10, pady=(10, 2), sticky=W)
        self._address_entry_frame.grid(row=1, column=1, padx=10, sticky=W)
        self._email_entry_frame.grid(row=2, column=1, padx=10, sticky=W)
        self._telephone_entry_frame.grid(row=3, column=1, padx=10, pady=(2, 10), sticky=W)

        self._selected_service: sv.Service | None = None

        self.focus_set()

    def validate_input_fields(self) -> False | pc.Postcode:
        """
        Validates the input fields that are provided for manual user input. By nature of the widget
        there is a facility provided for the user to auto-populate the fields with the information of
        services fetched by the database intermediary which should follow the same restrictions
        The return value is given as a boolean and not more in depth because this method assumes responsibility
        for alerting the user of their error and information surrounding it.

        :return: True if the input fields are valid, otherwise False
        """

        postcode = self._postcode_entry.get().replace(" ", "").upper()
        if not postcode.isalnum():
            messagebox.showerror("Uh Oh",
                                 "It looks like your postcode isn't a valid postcode. "
                                 "Double check it only contains numbers, letters from the alphabet, and spaces.")
            return False

        postcode_obj = self._dbc.command_able and self._dbc.get_postcode(postcode)
        if not postcode_obj:
            return False
        elif postcode_obj is dbc.DatabaseIntermediary.POSTCODE_NOT_EXIST:
            messagebox.showerror("Uh Oh",
                                 "It looks like your postcode isn't in our database of postcodes. "
                                 "Double check your postcode for any miniature errors")
            return False

        # validate email look

        if not EMAIL_REGEX.fullmatch(self._email_entry.get()):
            messagebox.showerror("Uh Oh",
                                 ""
                                 "")
            return False

        # validate telephone number look

        if not TELEPHONE_REGEX.fullmatch(self._email_entry.get()):
            messagebox.showerror("Uh Oh",
                                 ""
                                 "")
            return False

        return postcode_obj

    def get_selected_service(self) -> sv.Service | None:
        """
        Getter method for the service object representing the fields input by the user which may
        be a service object returned by the database intermediary or a new service object based on
        if the user has edited any of the input fields.
        If the input fields are invalid, then None will be returned

        :return: a service object; the service based on input fields. Or None if input fields are invalid
        """
        if postcode := self.validate_input_fields():
            if self._selected_service is None:
                return sv.Service(postcode=postcode, name=self._name_entry.get(), address_line_1=self._address_1_entry.get(), address_line_2=self._address_2_entry.get(), email=self._email_entry.get(), service_type=self._service_type)
            else:
                return self._selected_service

    def _button_return_service(self):
        service = self.get_selected_service()
        service and self._irc(service)

    def get_services(self, amount=10) -> tuple[sv.Service, ...] | None:
        """
        Simple service getter method which until reaching a result amount of either the given
        amount of services to find or all services there are to find, will repeatedly query
        the database intermediary for search results within (0.1 * n) longitude and latitude of the
        given postcode where n is the amount of times the method has had to grow it's search parameters.
        Because of this design choice, the method is more efficient the less results are required
        and the closer results are to the postcode.

        :param amount: the amount of services to get

        :return: a tuple of services found; or if the method couldn't query the databse intermediary, None
        """
        results: list[sv.Service, ...] = [...]
        last_results: list[sv.Service, ...] = []
        search_params = .1
        while len(results) < amount or len(last_results) != len(results):
            last_results = results
            if not self._dbc.command_able:
                messagebox.showerror("Uh Oh", "The program was unable to look for services")
                return
            results = self._dbc.get_services(self._service_type, self._postcode.longitude, self._postcode.latitude,
                                             loud=search_params, lold=search_params, laud=search_params, lald=search_params)
            search_params += .1
        return tuple(results)
