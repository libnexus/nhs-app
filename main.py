from __future__ import annotations

from tkinter import Tk, BOTH, YES, Entry, Frame, FIRST, END

import SQLDatabaseIntermediary as sqldbi
import application.gui.app as app
import application.gui.form as form
import application.util as util
from application.data.persistent_storage import APP_CONFIG
import application.gui.postcode_entry as pce
import application.gui.service_info_entry




root = Tk()
connector = sqldbi.DBConnector()
connector.init_db()
pce.PostcodeEntry(root, connector, lambda p: print("postcode", p))
a = app.App(root)
a.pack()
root.mainloop()

"""
util.repair_config_file()
APP_CONFIG.save()

# TODO reference https://konstantin.blog/2010/pickle-vs-json-which-is-faster/

connector = sqldbi.DBConnector()
connector.init_db()
LL57_1US = connector.get_services("GP", connector.get_postcode("LL571US"), 1)

main = app.App(root)
main_form = form.Form(main, LL57_1US)
main.add(main_form)
root.mainloop()
"""
