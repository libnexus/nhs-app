import application.data.postcode as postcode
import application.gui.service_info_entry as service_info_entry
from tkinter import Tk, Frame, BOTH, YES
import application.gui.service_listbox as service_listbox

root = Tk()


class F(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._service_info_entry = service_info_entry.ServiceInformationEntry(root,
                                                               postcode.Postcode("LL571US", -43.4, 5),
                                                               "SCHOOL",
                                                               None,
                                                               None)

main = F(root)
main.pack(fill=BOTH, expand=YES)

root.mainloop()