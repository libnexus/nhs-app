import application.postcodes.postcode as postcode
import application.gui.service_info_entry as service_info_entry
from tkinter import Tk, Frame, BOTH, YES

root = Tk()


class F(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._sie = service_info_entry.ServiceInformationEntry(root, "LL571US")


main = F(root)
main.pack(fill=BOTH, expand=YES)

root.mainloop()