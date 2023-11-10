from tkinter import Tk, Frame, BOTH, YES, LabelFrame, Entry, Menu
from tkinter.messagebox import showerror

import JSONDatabaseIntermediary as jdbi
from application.gui.service_info_entry import ServiceInformationEntry
from application.data.service import Service

root = Tk()


class Main(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._jdbi = jdbi.JSONDatabaseIntermediary()
        if not self._jdbi.init_db():
            showerror("Uh Oh", "The database had trouble connecting. Try restarting the program.")
            raise SystemExit
        self._service_info_entry = ServiceInformationEntry(root,
                                                           self._jdbi.get_postcode("LL572EH"),
                                                           "GP",
                                                           self._jdbi,
                                                           lambda o: print("returned", o))
        root.state("iconic")

        self._menu = Menu(root)


main = Main(root)
main.pack(fill=BOTH, expand=YES)

root.mainloop()
