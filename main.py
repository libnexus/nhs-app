from __future__ import annotations

from tkinter import Tk, BOTH, YES

import SQLDatabaseIntermediary as sqldbi
import application.gui.app as app
import application.gui.form as form
import application.util as util
from application.data.persistent_storage import APP_CONFIG

util.repair_config_file()
APP_CONFIG.save()

# TODO reference https://konstantin.blog/2010/pickle-vs-json-which-is-faster/

connector = sqldbi.DBConnector()
connector.init_db()
LL57_1US = connector.get_services("GP", connector.get_postcode("LL571US"), 1)

root = Tk()

main = app.App(root)
main_form = form.Form(main, LL57_1US)
main.add(main_form)
root.mainloop()
