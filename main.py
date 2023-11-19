from __future__ import annotations

from os.path import abspath
from tkinter import Tk, Frame, BOTH, YES, Menu
from tkinter.messagebox import showerror
from tkinter.ttk import Notebook

import JSONDatabaseIntermediary as jdbi
import application.gui.app as app
from application.data.service import Service

root = Tk()


main = app.App(root)
main.pack(fill=BOTH, expand=YES)

root.mainloop()
