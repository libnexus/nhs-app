import re as regex
from tkinter import Toplevel, Entry, Label, LabelFrame, Button, W, messagebox, NSEW, StringVar
from typing import Callable, Literal

import application.data.db_connector as dbc
import application.data.postcode as pc
import application.data.service as sv
import application.gui.service_listbox as service_listbox

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
        :param postcode: a postcode object to base search results on
        :param service_type: the type of service that the information entry is responsible for returning
        :param database_connector: the database intermediary the service information entry should use
        to fetch results
        :param info_return_callback:
        """
        super().__init__(master)

        # set up entry information

        self._postcode = postcode
        self._dbc = database_connector
        self._service_type = service_type
        self._irc = info_return_callback

        # set up entry as a top level

        self.resizable(False, False)
        self.title("Results for %s near %s (0)" % (self._service_type.capitalize() + "s", self._postcode.nice_postcode))

        # add services list

        self._service_listbox_frame = service_listbox.ServiceListbox(self, self.propagate_entry_fields, width=10)

        services = self.get_services()
        services = sorted(services, key=lambda s: s.postcode.distance_between(self._postcode))
        for service in services:
            self._service_listbox_frame.add_new_service(service)

        # add edit elements to entry

        self._name_entry_frame = LabelFrame(self, text="Name")
        self._name_field = StringVar()
        self._name_entry = Entry(self._name_entry_frame, width=43, textvariable=self._name_field)
        self._name_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        self._address_entry_frame = LabelFrame(self, text="Address")
        self._postcode_label = Label(self._address_entry_frame, text="Postcode")
        self._postcode_field = StringVar()
        self._postcode_entry = Entry(self._address_entry_frame, width=10, textvariable=self._postcode_field)
        self._address_1_label = Label(self._address_entry_frame, text="Address Line 1")
        self._address_1l1 = StringVar()
        self._address_1l2 = StringVar()
        self._address_2l1 = StringVar()
        self._address_2l2 = StringVar()
        self._address_1a_entry = Entry(self._address_entry_frame, width=29, textvariable=self._address_1l1)
        self._address_1b_entry = Entry(self._address_entry_frame, width=29, textvariable=self._address_1l2)
        self._address_2_label = Label(self._address_entry_frame, text="Address Line 2")
        self._address_2a_entry = Entry(self._address_entry_frame, width=29, textvariable=self._address_2l1)
        self._address_2b_entry = Entry(self._address_entry_frame, width=29, textvariable=self._address_2l2)

        self._postcode_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self._postcode_entry.grid(row=0, column=1, padx=(0, 10), sticky=W)
        self._address_1_label.grid(row=1, column=0, padx=5)
        self._address_1a_entry.grid(row=1, column=1, padx=(0, 10))
        self._address_1b_entry.grid(row=2, column=1, padx=(0, 10))
        self._address_2_label.grid(row=3, column=0)
        self._address_2a_entry.grid(row=3, column=1, padx=(0, 10))
        self._address_2b_entry.grid(row=4, column=1, padx=(0, 10), pady=(0, 10))

        self._email_entry_frame = LabelFrame(self, text="Email")
        self._email_field = StringVar()
        self._email_entry = Entry(self._email_entry_frame, width=43, textvariable=self._email_field)
        self._email_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        self._telephone_entry_frame = LabelFrame(self, text="Telephone")
        self._telephone_entry = Entry(self._telephone_entry_frame, width=43)
        self._telephone_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        self._service_listbox_frame.grid(row=0, column=0, rowspan=5, columnspan=3, padx=10, pady=10, sticky=NSEW)
        self._name_entry_frame.grid(row=0, column=4, padx=10, pady=(10, 2), sticky=W)
        self._address_entry_frame.grid(row=1, column=4, padx=10, sticky=W)
        self._email_entry_frame.grid(row=2, column=4, padx=10, sticky=W)
        self._telephone_entry_frame.grid(row=3, column=4, padx=10, sticky=W)

        # add submit button

        self._submit_button = Button(self, text="Submit", command=self._submit_service_form)
        self._submit_button.grid(row=4, column=4, columnspan=4, sticky=NSEW, padx=6, pady=(2, 10))

        self._selected_service: sv.Service | None = None

        self._submit_button.focus_set()

    def propagate_entry_fields(self, service: sv.Service):
        self._name_field.set(service.name)
        self._postcode_field.set(service.postcode.nice_postcode)
        self._email_field.set(service.email)


    def _submit_service_form(self):
        """

        """
        self.validate_input_fields()

    def validate_input_fields(self) -> Literal[False] | pc.Postcode:
        """
        Validates the input fields that are provided for manual user input. By nature of the widget
        there is a facility provided for the user to automatically populate the fields with the information of
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

        postcode_obj: bool | pc.Postcode = self._dbc.command_able and self._dbc.get_postcode(postcode)
        if not postcode_obj:
            return False
        elif postcode_obj is dbc.DatabaseIntermediary.POSTCODE_NOT_EXIST:
            messagebox.showerror("Uh Oh",
                                 "It looks like your postcode isn't in our database of data. "
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
                return sv.Service(postcode=postcode,
                                  name=self._name_entry.get(),
                                  address_line_1=self._address_1a_entry.get() + self._address_1b_entry.get(),
                                  address_line_2=self._address_2a_entry.get() + self._address_2b_entry.get(),
                                  email=self._email_entry.get(),
                                  service_type=self._service_type)
            else:
                return self._selected_service

    def _button_return_service(self):
        service = self.get_selected_service()
        service and self._irc(service)

    def get_services(self, amount=10) -> tuple[sv.Service, ...] | None:
        """
        Simple service getter method which until reaching a result amount of either the given
        amount of services to find or all services there are to find, will repeatedly query
        the database intermediary for search results within (1 * n) miles (converted to metres) of the
        given postcode where n is the amount of times the method has had to grow it's search parameters.
        Because of this design choice, the method is more efficient the less results are required
        and the closer results are to the postcode.


        :param amount: the amount of services to get

        :return: a tuple of services found; or if the method couldn't query the databse intermediary, None
        """
        results: list[sv.Service, ...] = [...]
        last_results: list[sv.Service, ...] = []
        search_params = 1
        while results != last_results:
            last_results = results
            if not self._dbc.command_able:
                messagebox.showerror("Uh Oh", "The program was unable to look for services")
                return
            results = self._dbc.get_services(self._service_type, self._postcode.longitude, self._postcode.latitude,
                                             distance=search_params * 1609, distance_from_postcode=self._postcode, max_number=amount)
            search_params += 1
        return tuple(results)
