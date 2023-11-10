from tkinter import Tk, Frame, BOTH, YES
from tkinter.messagebox import showerror

import JSONDatabaseIntermediary as jdbi
import application.data.postcode as postcode
import application.gui.service_info_entry as service_info_entry

root = Tk()


class F(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._jdbi = jdbi.JSONDatabaseIntermediary()
        if not self._jdbi.init_db():
            showerror("Uh Oh", "The database had trouble connecting. Try restarting the program.")
            raise SystemExit
        self._service_info_entry = service_info_entry.ServiceInformationEntry(root,
                                                                              self._jdbi.get_postcode("LL571US"),
                                                                              "SCHOOL",
                                                                              self._jdbi,
                                                                              lambda obj: print("returned", obj))
        root.state("iconic")


main = F(root)
main.pack(fill=BOTH, expand=YES)

root.mainloop()
