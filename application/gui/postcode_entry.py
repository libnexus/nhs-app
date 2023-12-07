from __future__ import annotations

from tkinter import messagebox, Toplevel, Entry, LabelFrame, StringVar, Button, END
from typing import Callable

import application.data.db_connector as dbc
import application.data.postcode as pc


class ShadowEntryWidget(Entry):
    def __init__(self, master, shadow_text: str, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._shadow_text = shadow_text
        self.insert(0, self._shadow_text)
        self.bind("<FocusIn>", self._clear)
        self.bind("<FocusOut>", self._regen)

    def _clear(self, e):
        if self.get() == self._shadow_text:
            self.delete(0, END)

    def _regen(self, e):
        if self.get() == "":
            self.insert(0, self._shadow_text)


class PostcodeEntry(Toplevel):
    def __init__(self, master,
                 database_connector: dbc.DatabaseIntermediary,
                 callback: Callable[[pc.Postcode], None]
                 ):
        super().__init__(master)
        # information entry
        self._postcode = pc.Postcode
        self._callback = callback

        self._dbc = database_connector

        self.resizable(False, False)
        self.title("Postcode Entry")

        # Postcode entry box

        self._postcode_entry_frame = LabelFrame(self, text="Postcode")
        self._postcode_field = StringVar()
        self._postcode_entry = ShadowEntryWidget(self._postcode_entry_frame,"e.g. ...", width=12, textvariable=self._postcode_field,
                                     font='Arial 20')
        self._postcode_entry.grid(row=0, column=0, padx=8, pady=4)
        self._postcode_entry_frame.pack()

        # submit button

        self._submit_button = Button(self._postcode_entry_frame, text="Submit", command=self._submit_postcode)
        self._submit_button.grid(row=1, column=0, pady=4)
        self._submit_button.focus_set()

    def _submit_postcode(self):
        postcode = self._postcode_field.get().replace(" ", "").upper()

        if self._dbc.get_postcode(postcode) == 0:
            # Returns True if retry is clicked, False if cancel is clicked
            retry = messagebox.askretrycancel(
                title='Postcode not found',
                message='The postcode was not found. Would you like to try again?'
            )
            if not retry:
                self.destroy()
        else:
            self._callback(self._dbc.get_postcode(postcode))
            self.destroy()
