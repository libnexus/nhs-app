from __future__ import annotations

from tkinter import Tk, messagebox

import SQLDatabaseIntermediary as sqldbi
import application.data.persistent_storage as pss
import application.data.service as sv
import application.gui.form as form
import application.gui.postcode_entry as pce


def __main__():
    root = Tk()
    connector = sqldbi.SQLDatabaseIntermediary()
    root.lower()
    if not connector.init_db():
        messagebox.showerror("Uh Oh", "Failed to connect to database.. Please try opening again.")
        return

    _found = False

    def __found_postcode__(_postcode):
        nonlocal _found

        _found = True
        main_form = form.Form(root, _postcode, connector)
        main_form.pack()

    def __bad_leave__(e):
        if not _found:
            raise SystemExit

    _pce = pce.PostcodeEntry(root, connector, __found_postcode__)
    _pce.bind("<Destroy>", __bad_leave__)
    root.winfo_toplevel().minsize()
    root.mainloop()


if __name__ == "__main__":
    __main__()