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
    pass # __main__()

if True:
    from json import loads

    data = loads(open(pss.safe_path("services-info.json"), "r").read())

    db = sqldbi.SQLDatabaseIntermediary()
    db.init_db()

    for postcode, services in data.items():
        for service in services:
            if isinstance(service["address"], list):
                service["address"] = ", ".join(service["address"])

            address = service["address"].split(", ")
            address1, address2 = ", ".join(address[:1]), ", ".join(address[1:])
            db.add_service(sv.Service(db.get_postcode(postcode), service["name"], address1, address2, service["email"],
                                      service["telephone"], service["type"].upper()))

    db.connection.commit()
    db.close_db()