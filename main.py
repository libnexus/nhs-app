from tkinter import Tk, Frame, BOTH, YES

import application.data.postcode as postcode
import application.gui.service_info_entry as service_info_entry

import JSONDatabaseIntermediary as jdbi

from tkinter.messagebox import showerror

root = Tk()


class F(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._jdbi = jdbi.JSONDatabaseIntermediary()
        if not self._jdbi.init_db():
            showerror("Uh Oh", "The database had trouble connecting. Try restarting the program.")
            raise SystemExit
        self._service_info_entry = service_info_entry.ServiceInformationEntry(root,
                                                                              postcode.Postcode("LL571US", -43.4, 5),
                                                                              "SCHOOL",
                                                                              self._jdbi,
                                                                              lambda obj: print("returned", obj))


main = F(root)
main.pack(fill=BOTH, expand=YES)
